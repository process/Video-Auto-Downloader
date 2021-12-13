'Simple util script for running dl script in background on Windows
Set objShell = WScript.CreateObject("WScript.Shell")
objShell.Run("dl.py"), 0, True