#!/usr/bin/env bash

if [ -z "${VIRTUAL_ENV}" ]; then
  echo "Make sure you run this script from within the"
  echo "Python Virtual environment of this project"
  exit 1
fi

if [ "$1" == "release" ] && [ ! -z "$(git diff --stat)" ]; then
  echo "Can not release as the project is 'dirty'."
  echo "Please make sure to commit everything before running a release build"
  exit 1
fi

has_create_dmg="$(which create-dmg)"
if [ -z "$has_create_dmg" ]; then
  echo "create-dmg is not installed."
  echo "if you want to make a release please make sure to install it first!"
  if [ "$1" == "release" ]; then
    exit 1
  fi
fi

if [ "$1" == "clean" ] || [ "$1" == "release" ]; then
  echo "Cleaning..."
  if [ -d "./dist" ]; then
    rm -rf "./dist" "./build" 2>/dev/null
  fi
fi

echo "Versioning..."
python ./version.py

echo "Building..."
./images.sh
python -OO -m PyInstaller --osx-bundle-identifier nl.ivonet.m4baker --noconsole -y m4baker.spec

echo "Tagging..."
./tag.sh

if [ "$1" == "release" ]; then
  echo "Packaging..."
  if [ -z "$has_create_dmg" ]; then
    echo "Not creating DMG release as create-dmg is not installed."
  else
    cd ./dist
    version=$(<../VERSION)
    create-dmg --app-drop-link 10 30  M4Baker_${version}.dmg M4Baker.app
    sha512sum "M4Baker_${version}.dmg" >"M4Baker_${version}.dmg.sha512"
  fi
fi
