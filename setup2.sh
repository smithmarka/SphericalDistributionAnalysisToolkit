#!/bin/bash

# Create a virtual environment
pyvenv-3.4 --without-pip .

# Download required files from the internet
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
chmod u+x get-pip.py

git clone https://github.com/scipy/scipy.git

# Activate the virtual environment to install pip
. bin/activate
which python

# Install pip and deactivate so that pip is available for use
./get-pip.py
deactivate
which python

# Activate pip and install the prerequisites
. bin/activate
which python

pip install --ignore-installed numpy
pip install --ignore-installed cython
pip install --ignore-installed matplotlib
pip install --ignore-installed pandas


# Install Scipy from source because the pip version is too old
cd scipy
git clean -xdf
python setup.py install

# Deactivate
which python
deactivate
which python
