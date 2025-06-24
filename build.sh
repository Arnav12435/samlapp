#!/usr/bin/env bash
set -o errexit  # Exit on error

# Update the package list
apt-get update

# Install system packages required by xmlsec
apt-get install -y libxml2-dev libxmlsec1-dev pkg-config xmlsec1 python3-dev
