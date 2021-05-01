#!/usr/bin/env bash
# simply move a file
#
# Attention: This is intended for use within target dataset.
#
# Needs a thorough consideration whether/how to generalize
# TODO: a bit of protection for too many/less arguments ...

set -e -u
set -x

datalad run --explicit --input "$1" --output "$2" mv "$1" "$2"
