#!/bin/bash


ssh -A -i ~/.ssh/main root@localhost -p 2222 'cd /root/gig/code/github/jumpscale/ays9; /bin/bash test.sh'
