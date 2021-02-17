#!/usr/bin/env bash

if [ -z "${VIRTUAL_ENV}" ]; then
    echo "Make sure you run this script from within the"
    echo "Python Virtual environment of this project"
    exit 1
fi

if [ "$1" == "clean" ]; then
  if [ -d "./dist"  ]; then
    rm -rf "./dist" 2>/dev/null
  fi
fi

pyinstaller --noconsole -y src/m4baker.py
