' 阿忠戰情表 — 無視窗啟動 (dashboard)
' 雙擊後：在背景啟動 serve.pyw（pythonw，完全無視窗），等 2 秒開瀏覽器
' 如果 server 已經在跑，新啟動的 pythonw 會因 port 被佔而安靜退出，無害
Option Explicit

Dim shell, fso, scriptDir, cmd
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = scriptDir

' 啟動 server（視窗樣式 0 = 隱藏，等待 = False 代表不阻塞）
cmd = "pythonw.exe """ & scriptDir & "\serve.pyw"""
shell.Run cmd, 0, False

' 等 server 起來再開瀏覽器
WScript.Sleep 2000
shell.Run "http://localhost:3000/index.html", 1, False
