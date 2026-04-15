@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "PORT=3000"
set "URL=http://localhost:%PORT%/index.html"

echo ==========================================
echo   ArChung Dashboard Launcher
echo ==========================================
echo.

REM --- Find Python ---
set "PY_CMD="
where py >nul 2>&1 && set "PY_CMD=py -3"
if not defined PY_CMD (
    where python >nul 2>&1 && set "PY_CMD=python"
)
if not defined PY_CMD (
    echo [X] Python 3 not found.
    echo.
    echo     Please install Python 3 first:
    echo     https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [i] Python: !PY_CMD!
echo.

REM --- Port already in use? Just open the browser. ---
netstat -ano | findstr "LISTENING" | findstr ":%PORT% " >nul 2>&1
if !errorlevel! equ 0 (
    echo [i] Port %PORT% is already in use. Opening dashboard...
    start "" "%URL%"
    timeout /t 2 /nobreak >nul
    exit /b 0
)

echo [^>] Starting server at %URL%
echo [^>] Keep this window open; closing it stops the server.
echo.

REM --- Schedule browser open 2s later via PowerShell ---
start "" /min powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process '%URL%'"

REM --- Start HTTP server (blocks this window) ---
!PY_CMD! -m http.server %PORT%

echo.
echo [i] Server stopped.
pause
