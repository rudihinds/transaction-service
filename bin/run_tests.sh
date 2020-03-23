#!/usr/bin/env sh

set -ex

pipenv run flake8
pipenv run python -m pytest;
pipenv run behave