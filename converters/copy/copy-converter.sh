#!/usr/bin/env bash
# simply copy a file and add it to destination dataset
# TODO: a bit of protection for too many/less arguments ...


set -e -u
set -x

if [ -d "$1" ]
then
    datalad run --explicit --input "$1" --output "$2"  cp -r "$1" "$2"
else
    datalad run --explicit --input "$1" --output "$2"  cp "$1" "$2"
fi
