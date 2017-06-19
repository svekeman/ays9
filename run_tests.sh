#!/bin/bash
echo "* Including js environment variables"
export SSHKEYNAME=main
source ~/.jsenv.sh
echo "* Start container"
js9_start
ssh -A -i ~/.ssh/main root@localhost -p 2222 'cd /root/gig/code/github/jumpscale/ays9; /bin/bash test.sh'
