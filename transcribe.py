"""
用 OpenAI Whisper API 產逐字稿。

用法：
    python transcribe.py <檔案路徑>

輸出：逐字稿純文字到 stdout。
錯誤：寫到 stderr，exit code 非 0。

需要環境變數 OPENAI_API_KEY。
定價：$0.006/分鐘（2026 年）。兩三分鐘的短片 ≈ $0.02。

限制：
- 單檔上限 25MB（OpenAI API 限制）。超過會 exit code 2 並提示。
- 支援格式：mp3, mp4, mpeg, mpga, m4a, wav, webm。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

MAX_BYTES = 25 * 1024 * 1024  # 25 MB


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python transcribe.py <file>", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 1

    size = path.stat().st_size
    if size > MAX_BYTES:
        print(
            f"file too large: {size / 1024 / 1024:.1f} MB (API 限制 25 MB)。\n"
            f"短影音應該不會超過，請確認是否誤放全集檔。",
            file=sys.stderr,
        )
        return 2

    if not os.environ.get("OPENAI_API_KEY"):
        print("missing env var OPENAI_API_KEY", file=sys.stderr)
        return 1

    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai", file=sys.stderr)
        return 1

    client = OpenAI()
    with open(path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="zh",
            response_format="text",
        )
    # response_format=text → result 是純字串
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
