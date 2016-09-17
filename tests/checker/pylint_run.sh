#!/bin/bash
export PYTHONPATH=${WORKSPACE}/tests/checker/plugins:${PYTHONPATH}
CHECK="*.py"

IGNORE="test,i18n,config"
echo $PYTHONPATH
CMD="pylint --ignore=${IGNORE}  --rcfile=${WORKSPACE}/tests/checker/pylintrc ${CHECK}"
echo $CMD
$CMD