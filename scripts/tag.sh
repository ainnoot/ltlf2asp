#! /usr/bin/bash

BUMP_RULE=$1
OLD_VERSION=$(poetry version -s)

poetry version $BUMP_RULE

NEW_VERSION=$(poetry version -s)

git add pyproject.toml
git commit -m "bump($BUMP_RULE): Bumping to $NEW_VERSION from $OLD_VERSION."
git tag -a v$NEW_VERSION -m "Tag for version $NEW_VERSION"
git push
git push origin tag v$NEW_VERSION
