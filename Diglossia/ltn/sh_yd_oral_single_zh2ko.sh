#!/usr/bin/env bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv deactivate
pyenv activate env_comm_Ana3-4.3.0
cd /search/chenguang/meng/SogouTrans/Diglossia/ltn/

nips=`ifconfig | grep "eth1.\d\d\d" -P -A 1 | grep "inet addr" | perl -ne "s/.*addr:| Bcast:.*//g;print;"`
echo "Number of vitural ip: " `echo $nips | sed "s/ /\n/g" | wc -l`

if [ -e pids_multi.txt ]; then
    for id in `cat pids_multi.txt`; do
        kill $id
    done
    rm pids_multi.txt
fi
self=$BASH_SOURCE
self=${self/sh/cmd}
cmd_file=${self/sh/py}
arr1=(${self//2/ })
arr2=(${arr1[0]//_/ })
arr3=(${arr1[1]//./ })
src=${arr2[4]}
tgt=${arr3[0]}

for ip in $nips; do
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    out_file="/search/chenguang/meng/logs/SogouTrans/"$ip"_"$src"2"$tgt".out"
    nohup python $cmd_file $src $tgt $ip > $out_file 2>&1 &
done