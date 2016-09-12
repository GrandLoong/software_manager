
set PYTHONPATH=%~dp0plugins;%PYTHONPATH%
echo 
set CHECK=*.py
set IGNORE=shotgun_api3,libs,yaml,i18n,QColorScheme
echo %PYTHONPATH%;
call C:\Users\Administrator\python27\Scripts\pylint.exe --ignore=%IGNORE% --rcfile=%~dp0pylintrc %CHECK%