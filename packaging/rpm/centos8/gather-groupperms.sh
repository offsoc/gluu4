#!/bin/bash

# Run this file after log into chroot
find / ! -type l ! -iname ".gitignore" ! -group root -printf "chgrp -R %g %h/%fn" | sort > /tmp/system_group.list
