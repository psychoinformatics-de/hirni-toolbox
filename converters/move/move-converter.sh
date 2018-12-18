#!/usr/bin/env bash
# simply git-move a file

set -e -u
set -x

datalad run --inputs "$1" --outputs "$2" git mv "$1" "$2"
