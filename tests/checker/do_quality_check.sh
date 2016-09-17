#!/bin/bash
cd ${WORKSPACE}
export PYLINTHOME=${WORKSPACE}/pylint_results
mkdir -p PYLINTHOME
rm *.stats
cp ~/.pylint.d/* ${PYLINTHOME}
${WORKSPACE}/tests/checker/pylint_run.sh > output.txt
${WORKSPACE}/tests/checker//trunk.py
x=$?
rm output.txt
exit $x
