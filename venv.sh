#!/usr/bin/env bash

usage() {
  echo "Usage: source $0"
  echo "A script that sets up a Python Virtualenv"
  exit 1
}

[ "$1" = "-h" ] && usage

version="$(<.python-version)"
IFS="." read -r major minor _ <<< "$version"

if ! python --version | grep -q "Python $major.$minor" ; then
  echo "Please use pyenv and install Python $major.$minor"
  return
fi

pyenv local "$major.$minor"

python -m venv venv || \
  return

. venv/bin/activate

pip install -r requirements.txt
