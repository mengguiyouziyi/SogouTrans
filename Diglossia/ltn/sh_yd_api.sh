#!/usr/bin/env bash
nips=`ifconfig | grep "eth1.\d\d\d" -P -A 1 | grep "inet addr" | perl -ne "s/.*addr:| Bcast:.*//g;print;"`
echo "Number of vitural ip: " `echo $nips | sed "s/ /\n/g" | wc -l`

if [ -e pids_multi.txt ]; then
    for id in `cat pids_multi.txt`; do
        kill $id
    done
    rm pids_multi.txt
fi

for ip in $nips; do
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    python ./cmd_yd_api.py $ip
done

