#!/bin/bash

#set -x
echo
echo Attempting to move core-dune files to /storage/ ...
echo
echo BEFORE:
/usr/bin/ssh  -q -o StrictHostKeyChecking=no <hostname> -v "ls -lrth /var/tmp/core-dune* && sudo /etc/init.d/dnsaproxy.dune status && sudo /usr/local/resolververify/testdigs.sh | grep 'SERVFAIL\|NOERROR\|NXDOMAIN' && dig @199.85.126.20 www.playboy.com && ps -eaf|grep dnsa && echo COMPRESSING FILES && time sudo gzip -9 /var/tmp/core-dune* && sudo mv /var/tmp/core-dune*.gz /storage/ || echo FILE DOESNT EXIST && echo; echo AFTER:;ls -lh /var/tmp/" > /tmp/dune_error_log_$date.log

