' Podcast 審核介面 — 無視窗啟動
' 雙擊後：在背景啟動 podcast-server.py（pythonw，無視窗），等 2 秒開瀏覽器
' 如果 server 已經在跑，新啟動的 pythonw 會因 port 被佔而安靜退出，無害
Option Explicit

Dim shell, fso, scriptDir, cmd
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = scriptDir

cmd = "pythonw.exe """ & scriptDir & "\podcast-server.py"""
shell.Run cmd, 0, False

WScript.Sleep 2000
shell.Run "http://localhost:3001/", 1, False
