@echo off
call "C:\Program Files\Nuke9.0v8\Nuke9.0.exe" --nukex  %1 || call "C:\Program Files\Nuke9.0v6\Nuke9.0.exe" --nukex %1
exit /B