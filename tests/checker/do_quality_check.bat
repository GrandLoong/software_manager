cd %WORKSPACE%
set PYLINTHOME=%WORKSPACE%/pylint_results
mkdir -p PYLINTHOME
deltree %PYLINTHOME%
%WORKSPACE%/tests/checker/pylint_run.bat > output.txt
python %WORKSPACE%/tests/checker//trunk.py
del %WORKSPACE%/output.txt
exit
