@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
cd /d "%~dp0"

set "PORT=3000"
set "URL=http://localhost:%PORT%/index.html"

echo ==========================================
echo   阿忠戰情表 Dashboard
echo ==========================================
echo.

REM --- 找 Python ---
set "PY_CMD="
where py >nul 2>&1 && set "PY_CMD=py -3"
if not defined PY_CMD (
    where python >nul 2>&1 && set "PY_CMD=python"
)
if not defined PY_CMD (
    echo [X] 找不到 Python 3
    echo.
    echo     請安裝後重試：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [i] Python: !PY_CMD!
echo.

REM --- 若 port 已被佔用（之前開過沒關），直接打開瀏覽器 ---
netstat -ano | findstr "LISTENING" | findstr ":%PORT% " >nul 2>&1
if !errorlevel! equ 0 (
    echo [i] Port %PORT% 已有 server，直接打開 dashboard
    start "" "%URL%"
    timeout /t 2 /nobreak >nul
    exit /b 0
)

echo [^>] 啟動 server: %URL%
echo [^>] 請勿關閉此視窗；關閉即停止 server
echo.

REM --- 用 PowerShell 排程 2 秒後開瀏覽器（避開 bat 嵌套引號地獄）---
start "" /min powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process '%URL%'"

REM --- 啟動 HTTP server（阻塞此視窗）---
!PY_CMD! -m http.server %PORT%

REM server 被 Ctrl+C 或關閉後會走到這
echo.
echo [i] Server 已停止
pause
