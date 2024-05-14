#! /usr/bin/bash

REF=$1
ACTOR=$2
REPO=$3
curl \
  -H "Title: CI/CD on ref $REF" \
  -H "Priority: default" \
  -H "X-Tags: o" \
  -d "A pipeline run for $REF@$REPO, started by $ACTOR on $REPO" \
  ntfy.sh/this-is-a-test-3456
