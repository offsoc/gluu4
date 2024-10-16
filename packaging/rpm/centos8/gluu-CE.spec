%global __os_install_post %{nil}
%define gluu_root /opt/gluu-server
%define _build_id_links none

Name: gluu-server
Version: 1
Release: 1.centos8
Summary: Gluu Server
Group: Gluu
License: Apache-2.0
Vendor: Gluu, Inc.
Packager: Gluu support <support@gluu.org>
Source0: gluu-server.tar.gz
Source1: gluu-serverd
Source2: systemd-unitfile
AutoReqProv: no
Requires: tar, systemd-container, sed, openssh, coreutils >= 8.22-12, systemd >= 208-20, initscripts >= 9.49.24-1

%description
Enterprise ready, free open source software for identity & access management (IAM).

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt
tar -xzf %{SOURCE0} -C %{buildroot}/opt
touch "%{buildroot}%{gluu_root}/tmp/system_user.list"
touch "%{buildroot}%{gluu_root}/tmp/system_group.list"
chmod 4777 "%{buildroot}%{gluu_root}/tmp"  
chmod 0755 "%{buildroot}%{gluu_root}/tmp/system_user.list" 
chmod 0755 "%{buildroot}%{gluu_root}/tmp/system_group.list"
# gluu-serverd
mkdir -p %{buildroot}/sbin/
/bin/cp %{SOURCE1} %{buildroot}/sbin/
# systemd unit file
mkdir -p %{buildroot}/lib/systemd/system/
/bin/cp %{SOURCE2} %{buildroot}/lib/systemd/system/systemd-nspawn@gluu-server.service

%pre
# Package is being updated
if [ $1 == 2 ]; then
    [ -e /opt/gluu-server/etc/passwd ] && cp -rp /opt/gluu-server/etc/passwd /opt/gluu-server/etc/passwd_upgrade || true
    [ -e /opt/gluu-server/etc/passwd- ] && cp -rp /opt/gluu-server/etc/passwd- /opt/gluu-server/etc/passwd-_upgrade || true
    [ -e /opt/gluu-server/etc/group ] && cp -rp /opt/gluu-server/etc/group /opt/gluu-server/etc/group_upgrade || true
    [ -e /opt/gluu-server/etc/group- ] && cp -rp /opt/gluu-server/etc/group- /opt/gluu-server/etc/group-_upgrade || true 
    [ -e /opt/gluu-server/etc/shadow ] && cp -rp /opt/gluu-server/etc/shadow /opt/gluu-server/etc/shadow_upgrade || true
    [ -e /opt/gluu-server/etc/shadow- ] && cp -rp /opt/gluu-server/etc/shadow- /opt/gluu-server/etc/shadow-_upgrade || true
    [ -e /opt/gluu-server/etc/gshadow ] && cp -rp /opt/gluu-server/etc/gshadow /opt/gluu-server/etc/gshadow_upgrade || true
    [ -e /opt/gluu-server/etc/gshadow- ] && cp -rp /opt/gluu-server/etc/gshadow- /opt/gluu-server/etc/gshadow-_upgrade || true
    [ -e /opt/gluu-server/etc/hostname ] && cp -rp /opt/gluu-server/etc/hostname  /opt/gluu-server/etc/hostname_upgrade || true  
    [ -e /opt/gluu-server/etc/hosts ] && cp -rp /opt/gluu-server/etc/hosts /opt/gluu-server/etc/hosts_upgrade || true
    [ -e /opt/gluu-server/etc/profile ] && cp -rp /opt/gluu-server/etc/profile /opt/gluu-server/etc/profile_upgrade || true
    [ -e /opt/gluu-server/etc/security/limits.conf ] && cp -rp /opt/gluu-server/etc/security/limits.conf /opt/gluu-server/etc/security/limits.conf_upgrade || true
    [ -e /opt/gluu-server/etc/sysconfig/network ] && cp -rp /opt/gluu-server/etc/sysconfig/network /opt/gluu-server/etc/sysconfig/network_upgrade || true
    [ -e /opt/gluu-server/etc/httpd/conf/httpd.conf ] && cp -rp /opt/gluu-server/etc/httpd/conf/httpd.conf /opt/gluu-server/etc/httpd/conf/httpd.conf_upgrade || true
fi

%post
/usr/sbin/chroot %{gluu_root} bash -c '
/tmp/system_user.list &>/dev/null
/tmp/system_group.list &>/dev/null 
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU &>/dev/null'
# systemd-nspawn container and keys
sed -i 's/.*Storage.*/Storage=persistent/g' /etc/systemd/journald.conf
systemctl restart systemd-journald
if [[ ! -d /var/lib/container ]]; then
  mkdir -p /var/lib/container
fi
ln -s %{gluu_root} /var/lib/container/gluu-server
if [[ -d /etc/gluu/keys ]]; then
  rm -rf /etc/gluu/keys
  mkdir -p /etc/gluu/keys
else
  mkdir -p /etc/gluu/keys
fi
ssh-keygen -b 2048 -t rsa -f /etc/gluu/keys/gluu-console -q -N ""
if [[ ! -d /opt/gluu-server/root/.ssh ]]; then
  mkdir -p /opt/gluu-server/root/.ssh
  chmod 700 /opt/gluu-server/root/.ssh
fi
cat /etc/gluu/keys/gluu-console.pub > /opt/gluu-server/root/.ssh/authorized_keys
chmod 600 /opt/gluu-server/root/.ssh/authorized_keys
cp -a /etc/resolv.conf /opt/gluu-server/etc/
systemctl enable machines.target
systemctl enable systemd-nspawn@gluu-server.service
# Running setup on package installation
if [ $1 == 1 ]; then
  echo "Starting gluu-server ..."
  sleep 1
  /sbin/gluu-serverd start
  sleep 10
  ssh -t -o IdentityFile=/etc/gluu/keys/gluu-console -o Port=60022 -o LogLevel=QUIET \
                -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                -o PubkeyAuthentication=yes root@localhost '/opt/gluu/bin/install.py'  
fi
# Package is being updated
if [ $1 == 2 ]; then
      if [ -e /opt/gluu-server/etc/gluu/conf ]; then
        [ -e /opt/gluu-server/etc/passwd_upgrade ] && mv /opt/gluu-server/etc/passwd_upgrade /opt/gluu-server/etc/passwd || true
        [ -e /opt/gluu-server/etc/passwd-_upgrade ] && mv /opt/gluu-server/etc/passwd-_upgrade /opt/gluu-server/etc/passwd- || true
        [ -e /opt/gluu-server/etc/group_upgrade ] && mv /opt/gluu-server/etc/group_upgrade /opt/gluu-server/etc/group || true
        [ -e /opt/gluu-server/etc/group-_upgrade ] && mv /opt/gluu-server/etc/group-_upgrade /opt/gluu-server/etc/group- || true 
        [ -e /opt/gluu-server/etc/shadow_upgrade ] && mv /opt/gluu-server/etc/shadow_upgrade /opt/gluu-server/etc/shadow || true 
        [ -e /opt/gluu-server/etc/shadow-_upgrade ] && mv /opt/gluu-server/etc/shadow-_upgrade /opt/gluu-server/etc/shadow- || true
        [ -e /opt/gluu-server/etc/gshadow_upgrade ] && mv /opt/gluu-server/etc/gshadow_upgrade /opt/gluu-server/etc/gshadow || true
        [ -e /opt/gluu-server/etc/gshadow-_upgrade ] && mv /opt/gluu-server/etc/gshadow-_upgrade /opt/gluu-server/etc/gshadow- || true
        [ -e /opt/gluu-server/etc/hostname_upgrade ] && mv /opt/gluu-server/etc/hostname_upgrade /opt/gluu-server/etc/hostname || true  
        [ -e /opt/gluu-server/etc/hosts_upgrade ] && mv /opt/gluu-server/etc/hosts_upgrade /opt/gluu-server/etc/hosts || true
        [ -e /opt/gluu-server/etc/profile_upgrade ] && mv /opt/gluu-server/etc/profile_upgrade /opt/gluu-server/etc/profile || true
        [ -e /opt/gluu-server/etc/security/limits.conf_upgrade ] && mv /opt/gluu-server/etc/security/limits.conf_upgrade /opt/gluu-server/etc/security/limits.conf || true
        [ -e /opt/gluu-server/etc/sysconfig/network_upgrade ] && mv /opt/gluu-server/etc/sysconfig/network_upgrade /opt/gluu-server/etc/sysconfig/network || true       
        [ -e /opt/gluu-server/etc/httpd/conf/httpd.conf_upgrade ] && mv /opt/gluu-server/etc/httpd/conf/httpd.conf_upgrade /opt/gluu-server/etc/httpd/conf/httpd.conf || true               
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/jetty ] && chown -R jetty:jetty /opt/jetty* || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/gluu/jetty ] && chown -R jetty:jetty /opt/gluu/jetty || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/gluu/jetty ] && chmod -R 755 /opt/gluu/jetty || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/shibboleth-idp ] && chown -R jetty:jetty /opt/shibboleth-idp || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/opendj ] && chown -R ldap:ldap /opt/opendj || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/node ] && chown -R node:node /opt/node* || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/gluu/node ] && chown -R node:node /opt/gluu/node || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/gluu/node ] && chmod -R 755 /opt/gluu/node || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/gluu/radius ] && chown -R radius:ldap /opt/gluu/radius || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /opt/gluu/radius ] && chmod -R a+rx /opt/gluu/radius || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /home/ldap ] && chown ldap:ldap /home/ldap || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /home/node ] && chown node:node /home/node || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /home/jetty ] && chown jetty:jetty /home/jetty || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/profile ] && chmod 644 /etc/profile || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /tmp ] && chmod ga+w /tmp || exit 0' 
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/gluu/ ] && chown root:gluu /var/gluu/ || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/gluu/ ] && chmod 755 /var/gluu/ || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/gluu/photos ] && chown root:gluu /var/gluu/photos || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/gluu/photos ] && chmod 775 /var/gluu/photos || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/gluu/identity ] && chown -R root:gluu /var/gluu/identity || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/gluu/identity ] && chmod -R 775 /var/gluu/identity || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run ] && chown root:root /var/run || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run/jetty ] && chown root:jetty /var/run/jetty || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run/jetty ] && chown jetty:jetty /var/run/jetty/* || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run/radius ] && chown root:root /var/run/radius || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run/ ] && chmod 755 /var/run/ || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run/jetty ] && chmod 775 /var/run/jetty || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run/jetty ] && chmod 644 /var/run/jetty/* || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /var/run/radius ] && chmod 775 /var/run/radius || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /install/community-edition-setup/output/oxauth-keys.json ] && chown jetty:jetty /install/community-edition-setup/output/oxauth-keys.json || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /install/community-edition-setup/output/oxauth-keys.json ] && chmod 500 /install/community-edition-setup/output/oxauth-keys.json || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/hostname ] && chmod 644 /etc/hostname || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/hosts ] && chmod 644 /etc/hosts || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /home/ldap/.pw ] && chown ldap:ldap /home/ldap/.pw || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/gluu/conf ] && chown root:gluu /etc/gluu/conf || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/init.d/opendj ] && chmod +x /etc/init.d/opendj || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/default/oxauth ] && chown root:root /etc/default/oxauth || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/init.d/oxauth ] && chmod +x /etc/init.d/oxauth || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /usr/lib/tmpfiles.d/jetty.conf ] && chown root:root /usr/lib/tmpfiles.d/jetty.conf || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /usr/lib/tmpfiles.d/jetty.conf ] && chmod 644 /usr/lib/tmpfiles.d/jetty.conf || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/default/identity ] && chown root:root /etc/default/identity || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/init.d/identity ] && chmod +x /etc/init.d/identity || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /usr/lib/tmpfiles.d/jetty.conf ] && chown root:root /usr/lib/tmpfiles.d/jetty.conf || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /usr/lib/tmpfiles.d/jetty.conf ] && chmod 644 /usr/lib/tmpfiles.d/jetty.conf || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/default/idp ] && chown root:root /etc/default/idp || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/init.d/idp ] && chmod +x /etc/init.d/idp || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /usr/lib/tmpfiles.d/jetty.conf ] && chown root:root /usr/lib/tmpfiles.d/jetty.conf || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /usr/lib/tmpfiles.d/jetty.conf ] && chmod 644 /usr/lib/tmpfiles.d/jetty.conf || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/default/passport ] && chown root:root /etc/default/passport || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/init.d/passport ] && chmod +x /etc/init.d/passport || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/init.d/gluu-radius ] && chmod +x /etc/init.d/gluu-radius || exit 0'
        /usr/sbin/chroot /opt/gluu-server /bin/su - root -c '[ -e /etc/gluu/conf/radius/ ] && chown root:gluu /etc/gluu/conf/radius/ || exit 0'
        /sbin/gluu-serverd stop
        /sbin/gluu-serverd start 
        sleep 30
      else
        if [ -z "$(ls -A /opt/gluu-server/install/community-edition-setup)" ]; then
            echo "Starting gluu-server ..."
            sleep 1
            /sbin/gluu-serverd start
            sleep 10
            ssh -t -o IdentityFile=/etc/gluu/keys/gluu-console -o Port=60022 -o LogLevel=QUIET \
                -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                -o PubkeyAuthentication=yes root@localhost '/opt/gluu/bin/install.py'  
        fi        
      fi     
fi

%preun
if [ $1 == 0 ]; then
      echo "Stopping Gluu Server ..."
      systemctl stop systemd-nspawn@gluu-server.service
fi 

%postun
if [ $1 == 0 ]; then
      if [ -d %{gluu_root}.rpm.saved ] ; then
           rm -rf %{gluu_root}.rpm.saved
      fi
      /bin/mv %{gluu_root} %{gluu_root}.rpm.saved
      echo "Your changes will be saved into %{gluu_root}.rpm.saved"
      rm -rf /etc/gluu/keys
      unlink /var/lib/container/gluu-server
      rm -rf /var/lib/container/gluu-server
      rm -rf /opt/gluu-server
      rm -rf /etc/systemd/system/machines.target.wants/systemd-nspawn@gluu-server.service
fi

%files
%{gluu_root}/*
%attr(755,root,root) /sbin/gluu-serverd
/lib/systemd/system/systemd-nspawn@gluu-server.service

%clean
rm -rf %{buildroot}

%changelog
* Thu May 02 2024 Ganesh Dutt Sharma <support@gluu.org> - 1-1
- new release
