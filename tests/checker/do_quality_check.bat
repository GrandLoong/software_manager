cd %WORKSPACE%
set PYLINTHOME=%WORKSPACE%\pylint_results
dir  pylint_results
%WORKSPACE%\tests\checker\pylint_run.bat > output.txt
python %WORKSPACE%\tests\checker\trunk.py
del %WORKSPACE%\output.txt
exit
