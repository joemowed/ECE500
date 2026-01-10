#!/bin/bash
if [[ -z "$VIRTUAL_ENV" ]]
then
    echo "Error: no virtual enviroment currently active">&2
    exit 1
fi
pip freeze > requirements.txt

