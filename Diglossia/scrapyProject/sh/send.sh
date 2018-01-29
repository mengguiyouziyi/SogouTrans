#!/usr/bin/env bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv deactivate
pyenv activate env_comm_Ana3-4.3.0
cd /search/chenguang/meng/SogouTrans/Diglossia/scrapyProject/util/

spider_name=$1
out_file="/search/chenguang/meng/logs/SogouTrans/send_"$spider_name".out"

echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
nohup python send.py $spider_name > $out_file 2>&1 &
echo "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
