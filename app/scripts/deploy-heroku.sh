#!/usr/bin/env bash

set -euxo pipefail

APP_DIR=app
HEROKU_REMOTE=heroku
BRANCH=master

git subtree push --prefix $APP_DIR $HEROKU_REMOTE $BRANCH
