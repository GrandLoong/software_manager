@echo off
start mshta vbscript:CreateObject("WScript.Shell").Run("cmd /c python software_manager.py",0,FALSE)(window.close)&&exit