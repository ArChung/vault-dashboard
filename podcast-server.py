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
from datetime import datetime
from pathlib import Path

import frontmatter
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

ROOT = Path(__file__).resolve().parent
DRAFTS_DIR = ROOT / "Brand" / "podcast-drafts"
ARCHIVE_DIR = DRAFTS_DIR / "archive"
INBOX_DIR = ROOT / "_PodcastInbox"

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

    # 刪原檔
    source = post.get("source_file")
    if source:
        src_path = (ROOT / source).resolve()
        if INBOX_DIR in src_path.parents and src_path.exists():
            src_path.unlink()

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

    return jsonify({"ok": True, "archived_to": str(archive_path.relative_to(ROOT))})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3001, debug=True)
