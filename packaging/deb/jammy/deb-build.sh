#!/bin/bash

# Define Paths
build_root="./gluu-server.amd64"

if [ "$1" != "" ]; then
    build_root=$1
fi

# Run Build
pushd $build_root
dpkg-buildpackage -us -uc
popd
