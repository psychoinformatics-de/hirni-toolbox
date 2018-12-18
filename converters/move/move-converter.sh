#!/usr/bin/env bash
# simply git-move a file

set -e -u
set -x

datalad run --explicit --input "$1" --output "$2" git mv "$1" "$2"
