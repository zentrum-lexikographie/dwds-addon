#!/bin/bash
set -xe

if [ -d "./venv" ]; then
  echo "venv already exists"
else
  echo "creating venv"
  python3 -m venv venv
fi

source ./venv/bin/activate
pip install -r requirements.txt

exit 0