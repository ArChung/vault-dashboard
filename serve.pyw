"""
Dashboard static file server with heartbeat + idle shutdown.

配合 dashboard.vbs 無視窗啟動：
- 提供 vault 根目錄的靜態檔案（index.html 等）
- 前端每 10 秒打一次 /__ping__
- 超過 IDLE_TIMEOUT 秒沒收到 ping 就自己結束（不靠視窗關閉）
- 重複啟動時若 port 已被佔用，會安靜退出（不擋後續開瀏覽器）

Run as: pythonw.exe serve.pyw
"""
from __future__ import annotations

import os
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 3000
IDLE_TIMEOUT = 60       # 秒，60 秒沒 ping 就退出
CHECK_INTERVAL = 10     # 秒，watchdog 檢查頻率

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)

_last_ping = time.monotonic()
_ping_lock = threading.Lock()


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # pythonw 沒 stdout，silence 免得內部 buffer 爆

    def do_GET(self):
        if self.path == '/__ping__':
            global _last_ping
            with _ping_lock:
                _last_ping = time.monotonic()
            self.send_response(204)
            self.end_headers()
            return
        return super().do_GET()


def _idle_watchdog():
    while True:
        time.sleep(CHECK_INTERVAL)
        with _ping_lock:
            idle = time.monotonic() - _last_ping
        if idle > IDLE_TIMEOUT:
            os._exit(0)


def main():
    threading.Thread(target=_idle_watchdog, daemon=True).start()
    try:
        with ThreadingHTTPServer(('127.0.0.1', PORT), Handler) as httpd:
            httpd.serve_forever()
    except OSError:
        # port 已被佔用（通常是另一個 instance 還活著），安靜退出即可
        sys.exit(0)


if __name__ == '__main__':
    main()
