#!/bin/bash

user=$2
host=$4

if [ ! $user ]; then
    echo Usage: `basename $0` --user yourname \(--host github.com\)
            exit
fi

if [ ! $host ]; then  
    host='github.com'  
fi  

user_prefix=$user.

ssh_key_file_name=$user_prefix$host.id_rsa
ssh_key_path=$HOME/.ssh/
ssh_config_path=$ssh_key_path'config'

echo
echo
echo
echo
echo
echo '开始生成ssh密钥对到'$HOME'/.ssh/目录'
echo
echo
echo
echo
echo


expect -c "spawn ssh-keygen -t rsa
expect \"Enter file in which\"
send \"$ssh_key_path$ssh_key_file_name\r\"
expect \"Enter passphrase\"
send \"\r\"
expect \"Enter same passphrase\"
send \"\r\"
expect eof"


echo '开始写入'$ssh_config_path'文件'

echo >> $ssh_config_path
echo 'Host '$host >> $ssh_config_path
if [ $user ]; then
    echo 'User '$user >> $ssh_config_path
fi
echo 'IdentityFile' $ssh_key_path$ssh_key_file_name >> $ssh_config_path
echo


echo
echo
echo
echo
echo
echo
echo '请把以下两行文字粘贴到http://icode.baidu.com/account/profile 中ssh 公钥部分'
cat $HOME/.ssh/$ssh_key_file_name.pub

chmod 600 $HOME/.ssh/*
#rm $HOME/.ssh/$ssh_key_file_name $HOME/.ssh/$ssh_key_file_name.pub


exit  

