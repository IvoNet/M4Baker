#!/usr/bin/env bash

if [ -z "${VIRTUAL_ENV}" ]; then
  echo "Make sure you run this script from within the"
  echo "Python Virtual environment of this project"
  exit 1
fi

python tools/wxGlade/wxglade.pyw
