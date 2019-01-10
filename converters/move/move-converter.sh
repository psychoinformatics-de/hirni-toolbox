#!/usr/bin/env bash
# simply git-move a file
# TODO: a bit of protection for too many/less arguments ...

set -e -u
set -x

datalad run --input "$1" git mv "$1" "$2"
