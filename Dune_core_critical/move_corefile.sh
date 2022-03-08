#!/bin/bash




echo
echo Attempting to move core files from /var/tmp to /storage/...
echo
echo BEFORE:
/usr/bin/ssh  -q -o StrictHostKeyChecking=no -i <ssh_key> "ls -lrth /var/tmp/core-dune* && sudo /etc/init.d/dnsaproxy.dune status && sudo mv /var/tmp/core-dune* /storage/ || echo FILE DOESNT EXIST && echo; echo AFTER:;ls -lh /var/tmp/"
