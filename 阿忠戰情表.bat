@echo off
REM 阿忠戰情表 — 本機啟動器
REM 雙點執行：開 python http.server 於 vault 目錄 + 用預設瀏覽器開 dashboard
REM 好處：優先讀本地檔、避開 GitHub API 流量限制、未 push 的改動也看得到

chcp 65001 > nul
cd /d "%~dp0"

set PORT=3000
set URL=http://localhost:%PORT%/index.html

REM 先檢查 port 是否已經被佔用（之前開過沒關）
netstat -ano | findstr ":%PORT% " | findstr "LISTENING" > nul
if %errorlevel% equ 0 (
    echo [i] Port %PORT% 已經有服務在跑，直接打開 dashboard
    start "" "%URL%"
    exit /b 0
)

REM 嘗試用 python 啟動（py launcher > python）
where py > nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=py -3
) else (
    where python > nul 2>&1
    if %errorlevel% equ 0 (
        set PY_CMD=python
    ) else (
        echo [X] 找不到 python，請先安裝 Python 3
        echo     下載：https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo [>] 啟動本機伺服器 on http://localhost:%PORT%
echo [>] 關閉此視窗即可停止 server

REM 2 秒後自動開瀏覽器（等 server 起來）
start "" cmd /c "timeout /t 2 /nobreak > nul && start %URL%"

REM 啟動 server（此視窗會一直佔用）
%PY_CMD% -m http.server %PORT%
