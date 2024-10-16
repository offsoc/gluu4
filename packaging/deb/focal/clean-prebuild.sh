#!/bin/bash
rm -rf *.changes
rm -rf *.deb
rm -rf *.dsc
rm -rf *.tar.gz
rm -rf *.buildinfo
rm -rf *.build
pushd ../gluu-server.amd64
debuild -- clean
popd

