#!/bin/bash



mins=120

echo
echo Attempting to purge arch files over $mins mins...
echo
echo BEFORE:
ssh  <hostname> "df -h; echo; sudo find /opt/neucap/prod/data/dmdarch/ -type f -mmin +$mins -exec rm -f {} \;;  sudo find /opt/neucap/prod/data/qnamearch/ -type f -mmin +$mins -exec rm -f {} \;;  sudo find /opt/neucap/prod/data/smplarch/ -type f -mmin +$mins -exec rm -f {} \;; echo AFTER:;df -h"
