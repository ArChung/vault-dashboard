"""
Podcast 審核介面的極簡後端。
- 讀寫 Brand/podcast-drafts/*.md（含 frontmatter）
- 前端：podcast-review.html
- Port: 3001

Dependencies: flask, flask-cors, python-frontmatter
    pip install flask flask-cors python-frontmatter
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

import frontmatter
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# ---- Heartbeat / idle shutdown 設定 ----
IDLE_TIMEOUT = 60      # 秒，超過這麼久沒 ping 就退出
CHECK_INTERVAL = 10    # 秒，watchdog 檢查頻率
_last_ping = time.monotonic()
_ping_lock = threading.Lock()

ROOT = Path(__file__).resolve().parent
DRAFTS_DIR = ROOT / "Brand" / "podcast-drafts"
ARCHIVE_DIR = DRAFTS_DIR / "archive"
# Google Drive「與我共用」加捷徑後的本機串流路徑
INBOX_DIR = Path(r"I:\.shortcut-targets-by-id\17Jr3DtGAN59oLGep2Cdsp1WhGsaYVZqN\夏日只想躺在家(完稿)")

CAPTION_HEADING = "## IG 文案"
TRANSCRIPT_HEADING = "## 逐字稿"

app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
CORS(app)


# ---------- MD 解析 ---------- #

def _split_sections(body: str) -> dict[str, str]:
    """把 MD body 按 '## 標題' 切成 {heading: content}。"""
    sections: dict[str, str] = {}
    current = "_preamble"
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            sections[current] = "\n".join(buf).strip()
            current = line.strip()
            buf = []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf).strip()
    return sections


def _rebuild_body(sections: dict[str, str], order: list[str]) -> str:
    """把 sections dict 組回 MD body，依 order 排列。"""
    parts: list[str] = []
    preamble = sections.get("_preamble", "").strip()
    if preamble:
        parts.append(preamble)
    for heading in order:
        if heading in sections:
            parts.append(f"{heading}\n\n{sections[heading]}".rstrip())
    return "\n\n".join(parts) + "\n"


def _load(slug: str, from_archive: bool = False) -> tuple[Path, frontmatter.Post, dict[str, str]]:
    base = ARCHIVE_DIR if from_archive else DRAFTS_DIR
    matches = list(base.glob(f"*{slug}.md"))
    if not matches:
        raise FileNotFoundError(slug)
    path = matches[0]
    post = frontmatter.load(path)
    sections = _split_sections(post.content)
    return path, post, sections


def _summarize(path: Path, post: frontmatter.Post) -> dict:
    sections = _split_sections(post.content)
    caption = sections.get(CAPTION_HEADING, "").strip()
    preview = caption[:80] + ("…" if len(caption) > 80 else "")
    return {
        "slug": post.get("slug") or path.stem,
        "filename": path.name,
        "source_file": post.get("source_file"),
        "created_at": post.get("created_at"),
        "status": post.get("status", "pending"),
        "caption_preview": preview,
    }


# ---------- API ---------- #

@app.get("/")
def index():
    return send_from_directory(str(ROOT), "podcast-review.html")


@app.get("/__ping__")
def ping():
    """前端 heartbeat，更新最後活動時間；配合 watchdog 自動收掉 idle server。"""
    global _last_ping
    with _ping_lock:
        _last_ping = time.monotonic()
    return ("", 204)


@app.get("/drafts")
def list_drafts():
    items = []
    for path in sorted(DRAFTS_DIR.glob("*.md")):
        try:
            post = frontmatter.load(path)
        except Exception:
            continue
        items.append(_summarize(path, post))
    # pending 排最前
    items.sort(key=lambda x: (x["status"] != "pending", x["created_at"] or ""), reverse=False)
    return jsonify(items)


@app.get("/drafts/<slug>")
def get_draft(slug: str):
    try:
        path, post, sections = _load(slug)
    except FileNotFoundError:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "slug": post.get("slug") or path.stem,
        "filename": path.name,
        "source_file": post.get("source_file"),
        "created_at": post.get("created_at"),
        "status": post.get("status", "pending"),
        "caption": sections.get(CAPTION_HEADING, "").strip(),
        "transcript": sections.get(TRANSCRIPT_HEADING, "").strip(),
    })


@app.patch("/drafts/<slug>")
def update_caption(slug: str):
    data = request.get_json(silent=True) or {}
    caption = (data.get("caption") or "").strip()
    try:
        path, post, sections = _load(slug)
    except FileNotFoundError:
        return jsonify({"error": "not found"}), 404

    sections[CAPTION_HEADING] = caption
    post.content = _rebuild_body(
        sections,
        order=[CAPTION_HEADING, TRANSCRIPT_HEADING],
    )
    with open(path, "wb") as f:
        frontmatter.dump(post, f)
    return jsonify({"ok": True})


@app.post("/approve/<slug>")
def approve(slug: str):
    try:
        path, post, sections = _load(slug)
    except FileNotFoundError:
        return jsonify({"error": "not found"}), 404

    caption = sections.get(CAPTION_HEADING, "").strip()
    if not caption:
        return jsonify({"error": "caption is empty, refuse to delete"}), 400

    # 刪 Drive 原檔（權限不足時警告但不擋流程）
    warnings = []
    source = post.get("source_file")
    if source:
        src_path = Path(source)
        if not src_path.is_absolute():
            src_path = (ROOT / source).resolve()
        try:
            if src_path.exists():
                src_path.unlink()
        except PermissionError:
            warnings.append(f"沒有刪除權限（檢視者？）：{src_path}")
        except OSError as e:
            warnings.append(f"刪檔失敗：{e}")

    # 搬 MD 到 archive/
    post["status"] = "deleted"
    post["approved_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    archive_path = ARCHIVE_DIR / path.name
    with open(archive_path, "wb") as f:
        frontmatter.dump(post, f)
    path.unlink()

    # commit + push（符合 vault auto-push 規則）
    try:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"podcast: approve + archive {slug}"],
            cwd=ROOT, check=True, capture_output=True,
        )
        subprocess.run(["git", "push"], cwd=ROOT, check=False, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # 沒變動或 push 失敗不擋流程

    return jsonify({
        "ok": True,
        "archived_to": str(archive_path.relative_to(ROOT)),
        "warnings": warnings,
    })


def _idle_watchdog():
    """60 秒沒 ping 就退出；搭配 podcast.vbs 無視窗啟動使用。"""
    while True:
        time.sleep(CHECK_INTERVAL)
        with _ping_lock:
            idle = time.monotonic() - _last_ping
        if idle > IDLE_TIMEOUT:
            os._exit(0)


if __name__ == "__main__":
    threading.Thread(target=_idle_watchdog, daemon=True).start()
    # debug=False：pythonw 沒 stdout，且 debug 模式的 auto-reload 會另開 process
    # 讓 watchdog 狀態亂掉
    app.run(host="127.0.0.1", port=3001, debug=False)
