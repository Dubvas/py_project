#!/bin/bash


pip install virtualenv>/dev/null
virtualenv venv>/dev/null
source venv/bin/activate>/dev/null

python3 dubcrypter.py "$@"