#!/usr/bin/env bash

VERSION=$(<./VERSION)

git add VERSION
git commit -m "v${VERSION}"

if [ -z "$(git diff --stat)" ]; then
  git tag "v${VERSION}"
  git push
  git push --tags
else
  echo "Git is dirty... not tagging a version"
  exit 1
fi
