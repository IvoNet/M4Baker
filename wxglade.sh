#!/usr/bin/env bash

if [ -z "${VIRTUAL_ENV}" ]; then
  echo "Make sure you run this script from within the"
  echo "Python Virtual environment of this project"
  exit 1
fi

rm -rf generated 2>/dev/null
mkdir generated 2>/dev/null

python tools/wxGlade/wxglade.pyw
