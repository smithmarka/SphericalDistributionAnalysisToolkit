#!/bin/bash

# Create a virtual environment
pyvenv-3.4 --without-pip .

# # Download required files from the internet
# curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
chmod u+x get-pip.py

# Activate the virtual environment to install pip
. bin/activate

# Install pip and deactivate so that pip is available for use
./get-pip.py
deactivate

# Activate pip and install the prerequisites
. bin/activate

pip install wheel
pip wheel --wheel-dir=./wheels -r requirements.txt

pip install --no-index --find-links=./wheels -r requirements.txt

deactivate