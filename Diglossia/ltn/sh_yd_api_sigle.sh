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
src='zh'
tgt='ja'
for ip in $nips; do
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    nohup python ./cmd_yd_api_single.py $src $tgt $ip > $ip"_"$src"-"$tgt".out" 2>&1 &
done

