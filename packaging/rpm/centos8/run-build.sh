#!/bin/bash

status=`pgrep rpm-build`
if [ "$status" != "" ]; then
    echo "process is running"
    exit 1
fi

./rpm-build.sh
