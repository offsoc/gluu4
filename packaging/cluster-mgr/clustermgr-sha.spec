Name:		clustermgr-sha
Version:	%VERSION%
Release:	%RELEASE%
Summary:	OAuth protected API
License:	The Gluu Support License
URL:  https://www.gluu.org
Source0:	clustermgr-sha-4.3.1.tgz
Source1:	clustermgr.service
Requires: python2

%description
Cluster Manager (CM) is a GUI tool for installing and managing a highly available, 
clustered Gluu Server infrastructure on physical servers or VMs

%prep
%setup -q

%install
mkdir -p %{buildroot}/tmp/
mkdir -p %{buildroot}/opt/
mkdir -p %{buildroot}/lib/systemd/system/
cp -a %{SOURCE1} %{buildroot}/lib/systemd/system/clustermgr.service
cp -a clustermgr %{buildroot}/opt/

%pre
mkdir -p /opt

%post
systemctl daemon-reload > /dev/null 2>&1
systemctl enable clustermgr > /dev/null 2>&1
rm -rf /usr/local/bin/clustermgr4-cli > /dev/null 2>&1
ln -s /opt/clustermgr/bin/clustermgr4-cli /usr/local/bin/clustermgr4-cli > /dev/null 2>&1

%preun
systemctl stop clustermgr > /dev/null 2>&1

%postun
if [ "$1" = 0 ]; then 
rm -rf /opt/clustermgr > /dev/null 2>&1
rm -rf /lib/systemd/system/clustermgr.service > /dev/null 2>&1
systemctl daemon-reload > /dev/null 2>&1
rm -rf /usr/local/bin/clustermgr4-cli > /dev/null 2>&1
fi

%files
/opt/clustermgr/*
/lib/systemd/system/clustermgr.service

%changelog
* Wed Apr 29 2020 Davit Nikoghosyan <davit@gluu.org> - %VERSION%-1
- Release %VERSION%
