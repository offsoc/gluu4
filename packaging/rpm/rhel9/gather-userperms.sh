#!/bin/bash

# Run this file after log into chroot
find / ! -type l ! -iname ".gitignore" ! -user root -printf "chown -R %u:%g %h/%fn" | sort > /tmp/system_user.list
