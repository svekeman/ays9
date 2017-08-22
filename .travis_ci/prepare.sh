#!/bin/bash

# generate ssh keys
ssh-keygen -t rsa -N "" -f ~/.ssh/main
export SSHKEYNAME=main

export GIGSAFE=1
export GIGDEVELOPERBRANCH=master

curl https://raw.githubusercontent.com/Jumpscale/developer/$GIGDEVELOPERBRANCH/jsinit.sh?$RANDOM > /tmp/jsinit.sh; bash /tmp/jsinit.sh

# build image
source ~/.jsenv.sh
source /tmp/.jsenv-functions.sh

export logfile=/tmp/install.log

dockerrun "jumpscale/js9base3" "base3" 2222

echo "[+] Updating jumpscale 9 libraries"
container "js9_getcode_libs_prefab_ays ${GIGBRANCH} noinit"
dockercommit "base3" "base3" "stop"

# js9_build -l
