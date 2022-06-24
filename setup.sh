#!/bin/bash

sudo apt update
xargs -a apt-requirements.txt sudo apt install

python3 -v venv venv
source venv/bin/activate

pip3 install -r requirements.txt