#!/bin/sh
version="4.5.1"
subversion="1"
if [ "x" != "x$subversion" ]; then
	new_dev_version="${version}-$subversion"
else
	new_dev_version="${version}"
fi
username="repo_user"
password='repo_pass'
os_version=$1

if [ $os_version = "18.04" ]; then
	os="ubuntu"
	os_name="bionic"
	deb_or_rpm="deb"
	prefix="Ub$os_version"
	extra_path="/gluu-server.amd64"
	extra_option=""
	cert_options=" update-ca-certificates --fresh; export SSL_CERT_DIR=/etc/ssl/certs; "
fi

if [ $os_version = "20.04" ]; then
	os="ubuntu"
	os_name="focal"
	deb_or_rpm="deb"
	prefix="Ub$os_version"
	extra_path="/gluu-server.amd64"
	extra_option=""
	cert_options=" update-ca-certificates --fresh; export SSL_CERT_DIR=/etc/ssl/certs; "
fi

if [ $os_version = "22.04" ]; then
	os="ubuntu"
	os_name="jammy"
	deb_or_rpm="deb"
	prefix="Ub$os_version"
	extra_path="/gluu-server.amd64"
	extra_option=""
	cert_options=" update-ca-certificates --fresh; export SSL_CERT_DIR=/etc/ssl/certs; "
fi

if [ $os_version = "centos7" ]; then
	os="centos"
	os_name="centos7"
	deb_or_rpm="rpm"
	prefix="Centos7"
	extra_path=""
	extra_option=""
	cert_options=""
fi

if [ $os_version = "centos8" ]; then
	os="centos"
	os_name="centos8"
	deb_or_rpm="rpm"
	prefix="Centos8"
	extra_path=""
	extra_option=""
	cert_options=""
fi

if [ $os_version = "rhel7" ]; then
	os="rhel"
	os_name="rhel7"
	deb_or_rpm="rpm"
	prefix="Rhel7"
	extra_path=""
	extra_option=" -k "
	cert_options=""
fi

if [ $os_version = "rhel8" ]; then
	os="rhel"
	os_name="rhel8"
	deb_or_rpm="rpm"
	prefix="Rhel8"
	extra_path=""
	extra_option=""
	cert_options=""
fi

echo "#!/bin/bash"
echo "rm -fr /tmp/Gluu-CE-$prefix"
echo "mkdir /tmp/Gluu-CE-$prefix/"
echo ""
echo "cp -pPr /home/jenkins/Gluu-CE-Chroot/gluu-ce-$deb_or_rpm-40 /tmp/Gluu-CE-$prefix/"
echo ""
echo "rm -fr /root/packaging"
echo "git clone -b version_$version https://github.com/GluuFederation/packaging"
echo ""
echo "mv packaging/$deb_or_rpm/$os_name/* /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40$extra_path/"
echo ""
echo "cd /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40$extra_path/"
echo "./clean-prebuild.sh"
echo ""
echo "cd /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40$extra_path/gluu-server"
echo "wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_$version/gluu_install.py"

echo "chroot /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40$extra_path/gluu-server /bin/bash -c \"$cert_options python3 gluu_install.py --no-setup -maven-user=\"$username\" -maven-password=\"$password\" -a $extra_option --jetty-version=10.0.15\""
echo "rm -fr gluu_install.py install/community-edition-setup/* /root/.bash_history"
echo ""
if [ $os = "ubuntu" ]; then
	### version can digest hyphen in ubuntu. So use at start.
	version=$new_dev_version
	echo "sed -i s/%VERSION%/\($version~$os$os_version\)/g /tmp/Gluu-CE-$prefix/gluu-ce-deb-40$extra_path/debian/changelog"
	echo "sed -i s/%VERSION%/$version~$os$os_version/g  /tmp/Gluu-CE-$prefix/gluu-ce-deb-40$extra_path/debian/postinst"
	echo "echo $version~$os$os_version > /tmp/Gluu-CE-$prefix/gluu-ce-deb-40$extra_path/gluu-server/etc/gluu-release"
	echo "sed -i s/%DIST%/$os_name/g /tmp/Gluu-CE-$prefix/gluu-ce-deb-40$extra_path/debian/changelog"
else
	echo "sed -i s/Version:\ 1/Version:\ $version/g /tmp/Gluu-CE-$prefix/gluu-ce-rpm-40/gluu-CE.spec"

	if [ "x" != "x$subversion" ]; then
		echo "sed -i s/Release:\ 1\.$os_version/Release:\ $subversion\.$os_version/g  /tmp/Gluu-CE-$prefix/gluu-ce-rpm-40/gluu-CE.spec"
	else
		echo "sed -i s/Release:\ 1\.$os_version/Release:\ $os_version/g  /tmp/Gluu-CE-$prefix/gluu-ce-rpm-40/gluu-CE.spec"
	fi
	### version can't digest hyphen in ubuntu. So use at this place.
	version=$new_dev_version
	echo "echo $version~$os_version > /tmp/Gluu-CE-$prefix/gluu-ce-rpm-40/gluu-server/etc/gluu-release"
fi
echo ""
echo ""
echo "cd /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40$extra_path && ./run-build.sh"
echo ""
echo ""
echo "sudo su jenkins -c \"cd /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40\""
if [ $os = "ubuntu" ]; then
	deb_name="gluu-server_$version~${os}${os_version}_amd64.deb"
	echo "sudo su jenkins -c \"scp /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40/$deb_name jenkins@repo.gluu.org:/tmp\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"cd /tmp && deb-sign-ce $deb_name\\\"\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"rm -f /var/www/html/ubuntu/pool/main/$os_name-devel/$deb_name\\\"\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"mv /tmp/$deb_name /var/www/html/ubuntu/pool/main/$os_name-devel/\\\"\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"cd /var/repo_scripts/ubuntu && ./updaterepo-$os_name-devel.sh\\\"\""

else
	if [ "x" != "x$subversion" ]; then
		rpm_name="gluu-server-$version.$os_name.x86_64.rpm"
	else
		rpm_name="gluu-server-$version-$os_name.x86_64.rpm"
	fi
	major_os_version="`echo $os_name|tr -d '[a-z]'`"
	echo "sudo su jenkins -c \"scp /tmp/Gluu-CE-$prefix/gluu-ce-$deb_or_rpm-40/rpmbuild/RPMS/x86_64/$rpm_name jenkins@repo.gluu.org:/tmp\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"cd /tmp && rpm --addsign $rpm_name\\\"\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"rm -f /var/www/html/$os/$major_os_version-testing/$rpm_name\\\"\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"mv /tmp/$rpm_name /var/www/html/$os/$major_os_version-testing/\\\"\""
	echo "sudo su jenkins -c \"ssh jenkins@repo.gluu.org \\\"cd /var/repo_scripts/$os && ./updaterepo-$major_os_version-testing.sh\\\"\""

fi
