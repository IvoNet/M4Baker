#!/usr/bin/env bash

VERSION=$(<./VERSION)

git add VERSION
git comit -m "v${VERSION}"
git tag v${VERSION}
git push --tags
