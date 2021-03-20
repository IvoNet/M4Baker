#!/usr/bin/env bash

if [ -z "${VIRTUAL_ENV}" ]; then
  echo "Make sure you run this script from within the"
  echo "Python Virtual environment of this project"
  exit 1
fi

if [ "$1" == "clean" ]; then
  echo "Cleaning..."
  if [ -d "./dist" ]; then
    rm -rf "./dist" "./build" 2>/dev/null
  fi
fi
echo "Versioning..."
python ./version.py

echo "Building..."

echo "Building the m4baker.app"
./images.sh
python -OO -m PyInstaller --osx-bundle-identifier nl.ivonet.m4baker --noconsole -y m4baker.spec

./tag.sh

check="$(which create-dmg)"
if [ -z "$check" ]; then
  echo "Not createing DMG as create-dmg is not installed."
else
  cd dist
  create-dmg --overwrite --dmg-title M4Baker M4Baker.app
  if [ -f "M4Baker 0.0.0.dmg" ]; then
    version= <../VERSION
    mv "M4Baker 0.0.0.dmg" "M4Baker_${version}".dmg

  fi
fi
