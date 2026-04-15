@echo off
REM 開 Podcast 審核介面：啟動 Flask server + 自動打開瀏覽器
REM 關掉視窗 = 停 server

cd /d "%~dp0"

REM 等 server 起來後自動開瀏覽器（背景 2 秒後開）
start "" /min cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:3001/"

echo.
echo ======================================
echo  Podcast 審核 server 啟動中 (port 3001)
echo  關掉這個視窗 = 停 server
echo ======================================
echo.

python podcast-server.py
