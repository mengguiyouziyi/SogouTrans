#!/usr/bin/env bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv deactivate
pyenv activate env_comm_Ana3-4.3.0
cd /search/chenguang/meng/SogouTrans/Diglossia/scrapyProject/

# get excuting-file name
#self=$(echo $0| awk -F "/" '{ print $NF }')
#spider_name=${self/.sh/}
#spider_name=${spider_name/sh_/}
spider_name=$1
cmd_file="cmd_yd_api"
#self=${self/sh/cmd}
#cmd_file=${self/sh/py}
#arr1=(${self//2/ })
#arr2=(${arr1[0]//_/ })
#arr3=(${arr1[1]//./ })
#src=${arr2[3]}
#tgt=${arr3[0]}

echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
o_file="/search/chenguang/meng/logs/SogouTrans/"$spider_name"_localhost.out"
nohup python $cmd_file $spider_name > $o_file 2>&1 &

# -------------------------------- 获取虚拟ip -----------------------------------
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
    i_p=${ip//./_}
    out_file="/search/chenguang/meng/logs/SogouTrans/"$spider_name"_"$i_p".out"
    nohup python $cmd_file $spider_name $ip > $out_file 2>&1 &
done