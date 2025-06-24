#!/usr/bin/env bash

# Update the package list
apt-get update

# Install required system packages
apt-get install -y libxml2-dev libxmlsec1-dev pkg-config python3-dev

# Install Python dependencies
pip install -r requirements.txt
