#!/bin/bash

# generate ssh keys
ssh-keygen -t rsa -N "" -f ~/.ssh/main
export SSHKEYNAME=main

export GIGSAFE=1
# export GIGBRANCH=$(git symbolic-ref --short HEAD)
export GIGBRANCH=master
export GIGDEVELOPERBRANCH=master

curl https://raw.githubusercontent.com/Jumpscale/developer/$GIGDEVELOPERBRANCH/jsinit.sh?$RANDOM > /tmp/jsinit.sh; bash /tmp/jsinit.sh

# build image
source ~/.jsenv.sh
js9_build -l

# install capnp tools
js9_start
ssh -A root@localhost -p 2222 "cd /tmp/;curl -O https://capnproto.org/capnproto-c++-0.6.1.tar.gz;tar zxf capnproto-c++-0.6.1.tar.gz;cd capnproto-c++-0.6.1;./configure;make install"
