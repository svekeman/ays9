#!/bin/bash
# echo "* Including js environment variables"
# export SSHKEYNAME=main
# source ~/.jsenv.sh
# echo "* Start container"
#
# js9_start
# # install capnp tools
# ssh -A -i ~/.ssh/main root@localhost -p 2222 "cd /tmp/;curl -O https://capnproto.org/capnproto-c++-0.6.1.tar.gz;tar zxf capnproto-c++-0.6.1.tar.gz;cd capnproto-c++-0.6.1;./configure;make install"
# # install RQ (http://python-rq.org/)
# ssh -A -i ~/.ssh/main root@localhost -p 2222 "pip install rq"
#
# # Run tests
# ssh -A -i ~/.ssh/main root@localhost -p 2222 'cd /root/gig/code/github/jumpscale/ays9; /bin/bash test.sh'

ZDockerActive -b jumpscale/ays9 -i ays9
ssh -tA  root@localhost -p 2222 "cd /tmp/;curl -O https://capnproto.org/capnproto-c++-0.6.1.tar.gz;tar zxf capnproto-c++-0.6.1.tar.gz;cd capnproto-c++-0.6.1;./configure;make install"
ssh -tA  root@localhost -p 2222 "pip install rq"
ssh -tA  root@localhost -p 2222 'cd /opt/code/github/jumpscale/ays9; /bin/bash test.sh'
