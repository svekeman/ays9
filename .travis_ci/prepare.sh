#!/bin/bash
set -e

# Install ays9 in a docker contianer using bash installers
sudo ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa
export SSHKEYNAME=id_rsa

export ZUTILSBRANCH=${ZUTILSBRANCH:-master}

curl https://raw.githubusercontent.com/Jumpscale/bash/$ZUTILSBRANCH/install.sh?$RANDOM > /tmp/install.sh;sudo -E bash /tmp/install.sh
sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad"
sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZInstall_ays9 -f"
