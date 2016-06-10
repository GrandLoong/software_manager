@echo off
mshta vbscript:createobject("wscript.shell").run("""%~dp0software_manager.py"" h",0)(window.close)&&exit