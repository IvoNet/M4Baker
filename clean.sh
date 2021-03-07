#!/usr/bin/env bash

echo "Cleaning project...."

rm -rf __pycache__ 2>/dev/null
rm -rf dist 2>/dev/null
rm -rf build 2>/dev/null
rm -rf generated 2>/dev/null
mkdir generated 2>/dev/null

echo "Finished."
