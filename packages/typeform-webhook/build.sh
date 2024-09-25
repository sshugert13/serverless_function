#!/bin/bash

set -e

cd "$(dirname "$0")"

# Create a virtual environment
virtualenv --without-pip virtualenv

# Install requirements
pip install -r requirements.txt --target virtualenv/lib/python3.11/site-packages

# Copy shared modules to the function package
cp -r ../shared .