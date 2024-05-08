#! /usr/bin/bash

BUMP_RULE=$1
OLD_VERSION=$(poetry version -s)
NEW_VERSION=$(poetry version $BUMP_RULE --dry-run -s)

git checkout -b release-v$NEW_VERSION
poetry version $BUMP_RULE
git add pyproject.toml
git commit -m "bump($BUMP_RULE): Bumping to $NEW_VERSION from $OLD_VERSION."
git commit --allow-empty -m "release: Releasing version v$NEW_VERSION."
git tag -a v$NEW_VERSION -m "Tag for version $NEW_VERSION"
git push --follow-tags
