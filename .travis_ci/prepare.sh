#!/bin/bash

# # generate ssh keys
# ssh-keygen -t rsa -N "" -f ~/.ssh/main
# export SSHKEYNAME=main
#
# export GIGSAFE=1
# export GIGDEVELOPERBRANCH=master
#
# curl https://raw.githubusercontent.com/Jumpscale/developer/$GIGDEVELOPERBRANCH/jsinit.sh?$RANDOM > /tmp/jsinit.sh; bash /tmp/jsinit.sh
#
# # build image
# source ~/.jsenv.sh
# js9_build -l
#

# docker using bash installers
sudo su -
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa

export ZUTILSBRANCH=fixes
export ZBRANCH=9.1.1_remove_gigdir
curl https://raw.githubusercontent.com/Jumpscale/bash/$ZUTILSBRANCH/install.sh?$RANDOM > /tmp/install.sh;sudo -E bash /tmp/install.sh
source /opt/code/github/jumpscale/bash/zlibs.sh
ZCodeGetJS
ZDockerInstallLocal
eval $(ssh-agent)
ssh-add
ZInstaller_js9_full
docker stop build
ZInstaller_ays9
