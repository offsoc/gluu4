### gluu-server-nochroot build (Ubuntu20)

## ssh to ubuntu20 build server
```
ssh root@pkg-deb4.gluu.org
```

## Update version and release 
```
vim ~/gluu-server-nochroot/debian/changelog
```

## go under nochroot folder and run build
```
cd ~/gluu-server-nochroot
./run-build.sh
```

## Move to repo server
```
cd gluu-ce-deb-40
scp gluu-server-nochroot_$VERSION~*.deb jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && deb-sign-ce gluu-server-nochroot_$VERSION~ubuntu20.04_amd64.deb"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/ubuntu/pool/main/focal-devel/gluu-server-nochroot_$VERSION-*.deb"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server-nochroot_$VERSION~ubuntu20.04_amd64.deb /var/www/html/ubuntu/pool/main/focal-devel/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/ubuntu && ./updaterepo-focal-devel.sh"
```



### gluu-server-nochroot build (Ubuntu18)

## ssh to ubuntu20 build server
```
ssh root@pkg-deb4.gluu.org
```

## Update version and release 
```
vim ~/gluu-server-nochroot/debian/changelog
```

## go under nochroot folder and run build
```
cd ~/gluu-server-nochroot
./run-build.sh
```

## Move to repo server
```
cd gluu-ce-deb-40
scp gluu-server-nochroot_$VERSION~*.deb jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && deb-sign-ce gluu-server-nochroot_$VERSION~ubuntu18.04_amd64.deb"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/ubuntu/pool/main/bionic-devel/gluu-server-nochroot_$VERSION-*.deb"
ssh jenkins@repo.gluu.org "mv /tmp/gluu-server-nochroot_$VERSION~ubuntu18.04_amd64.deb /var/www/html/ubuntu/pool/main/bionic-devel/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/ubuntu && ./updaterepo-bionic-devel.sh"
```


### gluu-server-nochroot build (centos7 and rhel7)

## ssh to centos8 build server
```
ssh root@pkg-rpm3.gluu.org
```

## Update version and release and dependency package list
```
vim ~/gluu-server-nochroot/gluu-server-nochroot.spec
(release should be el7 for centos7 and rhel7)
```

## Run build
```
cd ~/gluu-server-nochroot
./run-build.sh
```

## Move to repo server
```
scp rpmbuild/RPMS/x86_64/gluu-server-nochroot-$VERSION-*.rpm jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && rpm --addsign gluu-server-nochroot-$VERSION-centos7.x86_64.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/centos/7-testing/gluu-server-nochroot-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/rhel/7-testing/gluu-server-nochroot-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "cp /tmp/gluu-server-nochroot-$VERSION-centos7.x86_64.rpm /var/www/html/centos/7-testing/"
ssh jenkins@repo.gluu.org "cp /tmp/gluu-server-nochroot-$VERSION-centos7.x86_64.rpm /var/www/html/rhel/7-testing/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/centos && ./updaterepo-7-testing.sh"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/rhel && ./updaterepo-7-testing.sh"
```


### gluu-server-nochroot build (centos8 and rhel8)

## ssh to centos8 build server
```
ssh root@pkg-rpm3.gluu.org
```

## Update version and release and dependency package list
```
vim ~/gluu-server-nochroot/gluu-server-nochroot.spec
(release should be el8 for centos8 and rhel8)
```

## Run build
```
cd ~/gluu-server-nochroot
./run-build.sh
```

## Move to repo server
```
scp rpmbuild/RPMS/x86_64/gluu-server-nochroot-$VERSION-*.rpm jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && rpm --addsign gluu-server-nochroot-$VERSION-centos8.x86_64.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/centos/8-testing/gluu-server-nochroot-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/rhel/8-testing/gluu-server-nochroot-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "cp /tmp/gluu-server-nochroot-$VERSION-centos8.x86_64.rpm /var/www/html/centos/8-testing/"
ssh jenkins@repo.gluu.org "cp /tmp/gluu-server-nochroot-$VERSION-centos8.x86_64.rpm /var/www/html/rhel/8-testing/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/centos && ./updaterepo-8-testing.sh"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/rhel && ./updaterepo-8-testing.sh"
```


### gluu-server-nochroot build (suse15)

## ssh to suse15 build server
```
ssh root@suse15.gluu.org
```

## Update version and release and dependency package list
```
vim ~/gluu-server-nochroot/gluu-server-nochroot.spec
```

## Run build
```
cd ~/gluu-server-nochroot
./run-build.sh
```

## Move to repo server
```
scp rpmbuild/RPMS/x86_64/gluu-server-nochroot-$VERSION-*.rpm jenkins@repo.gluu.org:/tmp
ssh jenkins@repo.gluu.org "cd /tmp && rpm --addsign gluu-server-nochroot-$VERSION-15.x86_64.rpm"
ssh jenkins@repo.gluu.org "rm -f /var/www/html/suse/15-testing/gluu-server-nochroot-$VERSION-*.rpm"
ssh jenkins@repo.gluu.org "cp /tmp/gluu-server-nochroot-$VERSION-15.x86_64.rpm /var/www/html/suse/15-testing/"
ssh jenkins@repo.gluu.org "cd /var/repo_scripts/suse && ./updaterepo-15-testing.sh"
```

