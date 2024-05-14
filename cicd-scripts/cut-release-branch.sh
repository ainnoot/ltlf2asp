#! /usr/bin/bash

git checkout master
VERSION=$(poetry version -s)

git checkout -b release-v$VERSION
git commit --allow-empty -m "bump: This is a read-only branch for release v$VERSION."
git tag -a v$VERSION -m "New version: v$VERSION"
git push --follow-tags
