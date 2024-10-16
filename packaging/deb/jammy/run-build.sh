#!/bin/bash

status=`pgrep deb-build`
if [ "$status" != "" ]; then
    echo "Process is running"
    exit 1
fi

./deb-build.sh $1
