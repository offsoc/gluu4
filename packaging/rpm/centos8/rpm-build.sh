#!/bin/bash

# Define pathes
current_dir=`pwd`
gluu_ce_path="$current_dir"
rpmbuild_path="$current_dir/rpmbuild"

# Prepare build folders
mkdir -p $rpmbuild_path/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

# Spec file name
specfile=gluu-CE.spec

# Prepare sources
cd $gluu_ce_path

/bin/tar czf gluu-server.tar.gz --exclude=".gitignore" gluu-server
/bin/mv gluu-server.tar.gz $rpmbuild_path/SOURCES/
/bin/cp gluu-serverd $rpmbuild_path/SOURCES/gluu-serverd
/bin/cp systemd-unitfile $rpmbuild_path/SOURCES/systemd-unitfile
/bin/cp $specfile $rpmbuild_path/SPECS/

# Run build
QA_RPATHS=$[ 0x0001|0x0002 ] rpmbuild -ba --define "_topdir $rpmbuild_path" $rpmbuild_path/SPECS/$specfile 
