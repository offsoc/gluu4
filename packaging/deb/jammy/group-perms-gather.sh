#!/bin/bash

# Run this file after log into chroot
find / ! -type l ! -iname ".gitignore" ! -path "/proc/*" ! -path "/sys/*" ! -path "/dev/*" ! -group root -printf "chgrp -R %g %h/%f \n" | sort |uniq > system_group.list
