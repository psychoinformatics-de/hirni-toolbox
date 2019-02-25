#!/usr/bin/env bash
# simply git-move a file
# TODO: a bit of protection for too many/less arguments ...

set -e -u
set -x

datalad run --explicit --input "$1" --output "$2" git mv "$1" "$2"
