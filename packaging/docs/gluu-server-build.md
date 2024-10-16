### gluu-server build (Ubuntu20)

## ssh to ubuntu20 build server
```
ssh root@pkg-deb4.gluu.org
```

## copy chroot base to temp folder
```
cp -r /home/jenkins/Gluu-CE-Chroot/gluu-ce-deb-40 /tmp/Gluu-CE-Ub20.04/
```

## clone https://github.com/GluuFederation/packaging
```
git clone -b version_$VERSION https://github.com/GluuFederation/packaging
```

## Move packaging file to chroot
```
mv packaging/deb/focal/* /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/
```

## Run clean prebuild
```
cd /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/
./clean-prebuild.sh
```

## Get gluu_install.py and run it under chroot
```
cd /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/gluu-server
wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_$VERSION/gluu_install.py
chroot /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/gluu-server /bin/bash -c 'python3 gluu_install.py --no-setup -a --jetty-version=10.0.9'
rm gluu_install.py install/community-edition-setup/*
```

## Update version in changelog, postinst  and gluu-release
```
sed -i s/%VERSION%/\($VERSION~ubuntu20.04\)/g /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/debian/changelog
sed -i s/%VERSION%/$VERSION~ubuntu20.04/g  /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/debian/postinst
echo $VERSION~ubuntu20.04 > /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/gluu-server/etc/gluu-release
sed -i s/%DIST%/focal/g /tmp//Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/debian/changelog
```

## Run build
```
cd /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/ && ./run-build.sh
```

## Move to repo server
```
cd gluu-ce-deb-40
scp gluu-server_$VERSION~*.deb jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && deb-sign-ce gluu-server_$VERSION~ubuntu20.04_amd64.deb"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/ubuntu/pool/main/focal-devel/gluu-server_$VERSION-*.deb"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server_$VERSION~ubuntu20.04_amd64.deb /var/www/html/ubuntu/pool/main/focal-devel/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/ubuntu && ./updaterepo-focal-devel.sh"
```



### gluu-server build (Ubuntu18)

## ssh to ubuntu18 build server
```
ssh root@pkg-deb3.gluu.org
```

## copy chroot base to temp folder
```
cp -r /home/jenkins/Gluu-CE-Chroot/gluu-ce-deb-40 /tmp/Gluu-CE-Ub18.04/
```

## clone https://github.com/GluuFederation/packaging
```
git clone -b version_$VERSION https://github.com/GluuFederation/packaging
```

## Move packaging file to chroot
```
mv packaging/deb/bionic/* /tmp/Gluu-CE-Ub20.04/gluu-ce-deb-40/gluu-server.amd64/
```

## Run clean prebuild
```
cd /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/gluu-server.amd64/
./clean-prebuild.sh
```

## Get gluu_install.py and run it under chroot
```
cd /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/gluu-server.amd64/gluu-server
wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_$VERSION/gluu_install.py
chroot /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/gluu-server.amd64/gluu-server /bin/bash -c 'python3 gluu_install.py --no-setup -a --jetty-version=10.0.9'
rm gluu_install.py install/community-edition-setup/*
```

## Update version in changelog, postinst  and gluu-release
```
sed -i s/%VERSION%/\($VERSION~ubuntu18.04\)/g /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/gluu-server.amd64/debian/changelog
sed -i s/%VERSION%/$VERSION~ubuntu18.04/g  /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/gluu-server.amd64/debian/postinst
echo $VERSION~ubuntu18.04 > /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/gluu-server.amd64/gluu-server/etc/gluu-release
sed -i s/%DIST%/bionic/g /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/gluu-server.amd64/debian/changelog
```

## Run build
```
cd /tmp/Gluu-CE-Ub18.04/gluu-ce-deb-40/ && ./run-build.sh
```

## Move to repo server
```
cd gluu-ce-deb-40
scp gluu-server_$VERSION~*.deb jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && deb-sign-ce gluu-server_$VERSION~ubuntu18.04_amd64.deb"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/ubuntu/pool/main/bionic-devel/gluu-server_$VERSION-*.deb"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server_$VERSION~ubuntu18.04_amd64.deb /var/www/html/ubuntu/pool/main/bionic-devel/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/ubuntu && ./updaterepo-bionic-devel.sh"
```


### gluu-server build (centos7)

## ssh to centos7 build server
```
ssh root@pkg-rpm2.gluu.org
```

## copy chroot base to temp folder
```
cp -r /home/jenkins/Gluu-CE-Chroot/gluu-ce-rpm-40 /tmp/Gluu-CE-Centos7/
```

## clone https://github.com/GluuFederation/packaging
```
git clone -b version_$VERSION https://github.com/GluuFederation/packaging
```

## Move packaging file to chroot
```
mv packaging/rpm/centos7/* /tmp/Gluu-CE-Centos7/gluu-ce-rpm-40/
```

## Run clean prebuild
```
cd /tmp/Gluu-CE-Centos7/gluu-ce-rpm-40/
./clean-prebuild.sh
```

## Get gluu_install.py and run it under chroot
```
cd /tmp/Gluu-CE-Centos7/gluu-ce-rpm-40/gluu-server
wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_$VERSION/gluu_install.py
chroot /tmp/Gluu-CE-Centos7/gluu-ce-rpm-40/gluu-server /bin/bash -c 'python3 gluu_install.py --no-setup -a --jetty-version=10.0.9'
rm gluu_install.py install/community-edition-setup/*
```

## Update version/release in spec file
```
sed -i s/Version:\ 1/Version:\ $VERSION/g /home/jenkins/workspace/Gluu-CE-Centos7/gluu-ce-rpm-40/gluu-CE.spec
sed -i s/Release:\ 1\.centos7/Release:\ centos7/g /home/jenkins/workspace/Gluu-CE-Centos8/gluu-ce-rpm-40/gluu-CE.spec
echo $VERSION-centos7 > /home/jenkins/workspace/Gluu-CE-Centos7/gluu-ce-rpm-40/gluu-server/etc/gluu-release
```

## Run build
```
cd /home/jenkins/workspace/Gluu-CE-Centos7/gluu-ce-rpm-40/ && ./run-build.sh"
chown jenkins:jenkins /home/jenkins/workspace/Gluu-CE-Centos7/gluu-ce-rpm-40/rpmbuild/RPMS/x86_64/gluu-server-*.rpm"
```

## Move to repo server
```
cd gluu-ce-rpm-40/
scp rpmbuild/RPMS/x86_64/gluu-server-$VERSION-*.rpm jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && rpm --addsign gluu-server-$VERSION-centos7.x86_64.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/centos/7-testing/gluu-server-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server-$VERSION-centos7.x86_64.rpm /var/www/html/centos/7-testing/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/centos && ./updaterepo-7-testing.sh"
```


### gluu-server build (centos8)

## ssh to centos8 build server
```
ssh root@pkg-rpm3.gluu.org
```

## copy chroot base to temp folder
```
cp -r /home/jenkins/Gluu-CE-Chroot/gluu-ce-rpm-40 /tmp/Gluu-CE-Centos8/
```

## clone https://github.com/GluuFederation/packaging
```
git clone -b version_$VERSION https://github.com/GluuFederation/packaging
```

## Move packaging file to chroot
```
mv packaging/rpm/centos8/* /tmp/Gluu-CE-Centos8/gluu-ce-rpm-40/
```

## Run clean prebuild
```
cd /tmp/Gluu-CE-Centos8/gluu-ce-rpm-40/
./clean-prebuild.sh
```

## Get gluu_install.py and run it under chroot
```
cd /tmp/Gluu-CE-Centos8/gluu-ce-rpm-40/gluu-server
wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_$VERSION/gluu_install.py
chroot /tmp/Gluu-CE-Centos8/gluu-ce-rpm-40/gluu-server /bin/bash -c 'python3 gluu_install.py --no-setup -a --jetty-version=10.0.9'
rm gluu_install.py install/community-edition-setup/*
```

## Update version/release in spec file
```
sed -i s/Version:\ 1/Version:\ $VERSION/g /home/jenkins/workspace/Gluu-CE-Centos8/gluu-ce-rpm-40/gluu-CE.spec
sed -i s/Release:\ 1\.centos8/Release:\ centos8/g /home/jenkins/workspace/Gluu-CE-Centos8/gluu-ce-rpm-40/gluu-CE.spec
echo $VERSION-centos8 > /home/jenkins/workspace/Gluu-CE-Centos8/gluu-ce-rpm-40/gluu-server/etc/gluu-release
```

## Run build
```
cd /home/jenkins/workspace/Gluu-CE-Centos8/gluu-ce-rpm-40/ && ./run-build.sh"
chown jenkins:jenkins /home/jenkins/workspace/Gluu-CE-Centos8/gluu-ce-rpm-40/rpmbuild/RPMS/x86_64/gluu-server-*.rpm"
```

## Move to repo server
```
cd gluu-ce-rpm-40/
scp rpmbuild/RPMS/x86_64/gluu-server-$VERSION-*.rpm jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && rpm --addsign gluu-server-$VERSION-centos8.x86_64.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/centos/8-testing/gluu-server-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server-$VERSION-centos8.x86_64.rpm /var/www/html/centos/8-testing/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/centos && ./updaterepo-8-testing.sh"
```


### gluu-server build (rhel8)

## ssh to rhel8 build server
```
ssh root@pkg-rhel8.gluu.org
```

## copy chroot base to temp folder
```
cp -r /home/jenkins/Gluu-CE-Chroot/gluu-ce-rpm-40 /tmp/Gluu-CE-Rhel8/
```

## clone https://github.com/GluuFederation/packaging
```
git clone -b version_$VERSION https://github.com/GluuFederation/packaging
```

## Move packaging file to chroot
```
mv packaging/rpm/rhel8/* /tmp/Gluu-CE-Centos8/gluu-ce-rpm-40/
```

## Run clean prebuild
```
cd /tmp/Gluu-CE-Rhel8/gluu-ce-rpm-40/
./clean-prebuild.sh
```

## Get gluu_install.py and run it under chroot
```
cd /tmp/Gluu-CE-Rhel8/gluu-ce-rpm-40/gluu-server
wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_$VERSION/gluu_install.py
chroot /tmp/Gluu-CE-Rhel8/gluu-ce-rpm-40/gluu-server /bin/bash -c 'python3 gluu_install.py --no-setup -a --jetty-version=10.0.9'
rm gluu_install.py install/community-edition-setup/*
```

## Update version/release in spec file
```
sed -i s/Version:\ 1/Version:\ $VERSION/g /home/jenkins/workspace/Gluu-CE-Rhel8/gluu-ce-rpm-40/gluu-CE.spec
sed -i s/Release:\ 1\.rhel8/Release:\ rhel8/g /home/jenkins/workspace/Gluu-CE-Rhel8/gluu-ce-rpm-40/gluu-CE.spec
echo $VERSION-rhel8 > /home/jenkins/workspace/Gluu-CE-Rhel8/gluu-ce-rpm-40/gluu-server/etc/gluu-release
```

## Run build
```
cd /home/jenkins/workspace/Gluu-CE-Rhel8/gluu-ce-rpm-40/ && ./run-build.sh"
chown jenkins:jenkins /home/jenkins/workspace/Gluu-CE-Rhel8/gluu-ce-rpm-40/rpmbuild/RPMS/x86_64/gluu-server-*.rpm"
```

## Move to repo server
```
cd gluu-ce-rpm-40/
scp rpmbuild/RPMS/x86_64/gluu-server-$VERSION-*.rpm jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && rpm --addsign gluu-server-$VERSION-rhel8.x86_64.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/rhel/8-testing/gluu-server-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server-$VERSION-rhel8.x86_64.rpm /var/www/html/rhel/8-testing/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/rhel && ./updaterepo-8-testing.sh"
```


### gluu-server build (rhel7)

## ssh to rhel7 build server
```
ssh root@pkg-rhel7.gluu.org
```

## copy chroot base to temp folder
```
cp -r /home/jenkins/Gluu-CE-Chroot/gluu-ce-rpm-40 /tmp/Gluu-CE-Rhel7/
```

## clone https://github.com/GluuFederation/packaging
```
git clone -b version_$VERSION https://github.com/GluuFederation/packaging
```

## Move packaging file to chroot
```
mv packaging/rpm/rhel7/* /tmp/Gluu-CE-Rhel7/gluu-ce-rpm-40/
```

## Run clean prebuild
```
cd /tmp/Gluu-CE-Rhel7/gluu-ce-rpm-40/
./clean-prebuild.sh
```

## Get gluu_install.py and run it under chroot
```
cd /tmp/Gluu-CE-Rhel7/gluu-ce-rpm-40/gluu-server
wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_$VERSION/gluu_install.py
chroot /tmp/Gluu-CE-Rhel7/gluu-ce-rpm-40/gluu-server /bin/bash -c 'python3 gluu_install.py --no-setup -a --jetty-version=10.0.9'
rm gluu_install.py install/community-edition-setup/*
```

## Update version/release in spec file
```
sed -i s/Version:\ 1/Version:\ $VERSION/g /home/jenkins/workspace/Gluu-CE-Rhel7/gluu-ce-rpm-40/gluu-CE.spec
sed -i s/Release:\ 1\.rhel7/Release:\ rhel7/g /home/jenkins/workspace/Gluu-CE-Rhel7/gluu-ce-rpm-40/gluu-CE.spec
echo $VERSION-rhel7 > /home/jenkins/workspace/Gluu-CE-Rhel7/gluu-ce-rpm-40/gluu-server/etc/gluu-release
```

## Run build
```
cd /home/jenkins/workspace/Gluu-CE-Rhel7/gluu-ce-rpm-40/ && ./run-build.sh"
chown jenkins:jenkins /home/jenkins/workspace/Gluu-CE-Rhel7/gluu-ce-rpm-40/rpmbuild/RPMS/x86_64/gluu-server-*.rpm"
```

## Move to repo server
```
cd gluu-ce-rpm-40/
scp rpmbuild/RPMS/x86_64/gluu-server-$VERSION-*.rpm jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && rpm --addsign gluu-server-$VERSION-rhel7.x86_64.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/rhel/8-testing/gluu-server-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server-$VERSION-rhel7.x86_64.rpm /var/www/html/rhel/8-testing/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/rhel && ./updaterepo-8-testing.sh"
```

