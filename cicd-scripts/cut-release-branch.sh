#! /usr/bin/bash

VERSION=$(poetry version -s)

git checkout -b release-v$VERSION
git commit --allow-empty -m "release: Read-only branch for release v$VERSION."
git tag -a v$VERSION -m "New version: v$VERSION"
git push --follow-tags
