#!/bin/bash

# Run this file after log into chroot
find / ! -type l ! -iname ".gitignore" ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" ! -user root -printf "chown -R %u:%g %h/%f \n"|sort |uniq > system_user.list
