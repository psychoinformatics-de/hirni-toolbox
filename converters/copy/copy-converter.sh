#!/usr/bin/env bash
# simply copy a file and add it to destination dataset
#
# Usage: <script> <source> <destination> <follow|dont-follow>
#
# Default: follow
#          follow links in <source> in order to copy content rather than the
#          link
#
#
# TODO: a bit of protection for too many/less arguments ...


set -e -u
set -x

# TODO: Better do proper option evaluation.
if [[ ${3:-follow} == "follow" ]];
then
    follow_opt="-L"
else
    follow_opt=""
fi

if [ -d "$1" ]
then
    datalad run --explicit --input ${1} --output ${2}  cp ${follow_opt} -r ${1} ${2}
else
    datalad run --explicit --input ${1} --output ${2}  cp ${follow_opt} ${1} ${2}
fi
