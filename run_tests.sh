#!/bin/bash
echo "* Including js environment variables"
export SSHKEYNAME=main
source ~/.jsenv.sh
echo "* Start container"

js9_start
# install capnp tools
ssh -A -i ~/.ssh/main root@localhost -p 2222 "cd /tmp/;curl -O https://capnproto.org/capnproto-c++-0.6.1.tar.gz;tar zxf capnproto-c++-0.6.1.tar.gz;cd capnproto-c++-0.6.1;./configure;make install"
# install RQ (http://python-rq.org/)
ssh -A -i ~/.ssh/main root@localhost -p 2222 "pip install rq"

# start rq worker
ssh -A -i ~/.ssh/main root@localhost -p 2222 "js9 \"j.tools.prefab.get().tmux.executeInScreen('main', 'rq', cmd='rq worker', wait=0)\""

ssh -A -i ~/.ssh/main root@localhost -p 2222 'cd /root/gig/code/github/jumpscale/ays9; /bin/bash test.sh'
