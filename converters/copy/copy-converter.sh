#!/usr/bin/env bash
# simply copy a file and add it to destination dataset

set -e -u
set -x

if [ -d "$1" ]
then
    datalad run --input "$1" --output "$2" cp -r "$1" "$2"
else
    datalad run --input "$1" --output "$2" cp "$1" "$2"
fi
