#!/usr/bin/env bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv deactivate
pyenv activate env_comm_Ana3-4.3.0
cd /search/chenguang/meng/SogouTrans/Diglossia/ltn/util/

self=$BASH_SOURCE
o_file=${self/sh/out}
out_file="/search/chenguang/meng/logs/SogouTrans/"$o_file
spider_name=${self/send_/}
spider_name=${spider_name/.sh/}
request_key=$spider_name":requests"
i_file="oral800w.zh"
in_file="/search/chenguang/meng/documents/SogouTrans/"$i_file

echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
nohup python send.py $in_file $request_key > $out_file 2>&1 &
echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
