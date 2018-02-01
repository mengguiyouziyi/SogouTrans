#!/usr/bin/env bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv deactivate
pyenv activate env_comm_Ana3-4.3.0
cd /search/chenguang/meng/SogouTrans/Diglossia/scrapyProject/

spider_name=$1
cmd_file="cmd.py"
ip=$2

echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
i_p=${ip//./_}
out_file="/search/chenguang/meng/logs/SogouTrans/"$spider_name"_"$i_p".out"
nohup python $cmd_file $spider_name $ip >> $out_file 2>&1 &