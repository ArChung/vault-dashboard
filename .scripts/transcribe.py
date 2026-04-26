"""
用 OpenAI Whisper API 產逐字稿。影片會先用 ffmpeg 抽音訊壓成 mp3。

用法：
    python transcribe.py <檔案路徑>

輸出：逐字稿純文字到 stdout。
錯誤：寫到 stderr，exit code 非 0。

需要：
- 環境變數 OPENAI_API_KEY
- ffmpeg 在 PATH

定價：$0.006/分鐘（2026 年）。

流程：
1. 若是 mp3 / m4a / wav 且 <25MB → 直接上傳
2. 否則用 ffmpeg 抽音軌壓成 32kbps mono mp3 到暫存 → 上傳 → 刪暫存
   （32kbps 對語音足夠，45 分鐘影片壓完約 11MB）
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

MAX_BYTES = 25 * 1024 * 1024  # 25 MB
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".mpga", ".mpeg"}


def compress_to_mp3(src: Path, dst: Path) -> None:
    """用 ffmpeg 抽音軌 + 壓成 32kbps mono mp3。失敗丟 RuntimeError。"""
    cmd = [
        "ffmpeg", "-y",
        "-i", str(src),
        "-vn",              # 丟掉 video
        "-ac", "1",         # mono
        "-ar", "16000",     # 16kHz（Whisper 內部就用這 rate，再高沒差）
        "-b:a", "32k",      # 32kbps，語音夠用
        "-f", "mp3",
        str(dst),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg 失敗：\n{result.stderr[-2000:]}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python transcribe.py <file>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1

    if not os.environ.get("OPENAI_API_KEY"):
        print("missing env var OPENAI_API_KEY", file=sys.stderr)
        return 1

    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai", file=sys.stderr)
        return 1

    # 決定要上傳的檔案
    upload_path = path
    tmp: Path | None = None

    needs_compression = (
        path.suffix.lower() not in AUDIO_EXTS
        or path.stat().st_size > MAX_BYTES
    )

    if needs_compression:
        # 檢查 ffmpeg 有沒有
        if subprocess.run(["ffmpeg", "-version"], capture_output=True).returncode != 0:
            print("ffmpeg 不在 PATH，請先裝 ffmpeg", file=sys.stderr)
            return 1

        _fd, _tmp_name = tempfile.mkstemp(suffix=".mp3", prefix="whisper_")
        os.close(_fd)  # Windows 鎖檔：一定要關 fd，不然後面 unlink 會 PermissionError
        tmp = Path(_tmp_name)
        print(f"→ ffmpeg 壓縮中：{path.name}", file=sys.stderr)
        try:
            compress_to_mp3(path, tmp)
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            tmp.unlink(missing_ok=True)
            return 1

        size = tmp.stat().st_size
        print(f"  壓縮後 {size / 1024 / 1024:.1f} MB", file=sys.stderr)
        if size > MAX_BYTES:
            print(
                f"壓縮後仍 >25MB（{size / 1024 / 1024:.1f} MB）。"
                f"檔案可能很長，請切段或手動處理。",
                file=sys.stderr,
            )
            tmp.unlink(missing_ok=True)
            return 2
        upload_path = tmp

    try:
        client = OpenAI()
        print(f"→ 上傳 Whisper API：{upload_path.name}", file=sys.stderr)
        with open(upload_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="zh",
                response_format="text",
            )
        print(result)
        return 0
    finally:
        if tmp:
            tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
