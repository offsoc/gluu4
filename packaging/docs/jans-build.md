### 1. SSH to server
```
Ubuntu
ssh root@pkg-deb4.gluu.org

el8
ssh root@pkg-rpm3.gluu.org 

Suse
ssh root@suse15.gluu.org
```

### 2. go to juns folder and run run-build.sh
```
cd jans
./run-build.sh
```

### 3. Remove previous builds
```
ssh  root@repo.gluu.org -- rm /var/www/html/jans/*
```

### 4. Move new builds to repo.gluu.org
```
Ubuntu
scp jans_1.0.0~ubuntu20.04_amd64.deb root@repo.gluu.org:/var/www/html/jans  

EL8
scp rpmbuild/RPMS/x86_64/jans-1.0.0-el8.x86_64.rpm root@repo.gluu.org:/var/www/html/jans

Suse
scp rpmbuild/RPMS/x86_64/jans-1.0.0-suse15.x86_64.rpm root@repo.gluu.org:/var/www/html/jans
```
