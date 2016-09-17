#!/bin/bash
cd ${WORKSPACE}
export PYLINTHOME=${WORKSPACE}/pylint_results
mkdir -p PYLINTHOME
sudo rm *.stats
cp ~/.pylint.d/* ${PYLINTHOME}
chmod +x ${WORKSPACE}/tests/checker/pylint_run.sh
${WORKSPACE}/tests/checker/pylint_run.sh > output.txt
chmod +x ${WORKSPACE}/tests/checker/trunk.py
${WORKSPACE}/tests/checker/trunk.py
x=$?
rm output.txt
exit $x
