#!/usr/bin/env bash

VERSION=$(<./VERSION)

if [[ $(git diff --stat) != '' ]]; then
  echo 'dirty'
else
  echo 'clean'
fi

git add VERSION
git commit -m "v${VERSION}"
git push
git tag "v${VERSION}"
git push --tags
