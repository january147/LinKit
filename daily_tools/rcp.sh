#!/bin/bash
# Date: Sat Oct 26 21:12:19 2019
# Author: January

set -o errexit
######################config######################
remote_dir="root@39.108.170.44:/root/store"


function rcp_send(){
    local_path=$1
    remote_path="$remote_dir/${2#/}"
    scp "$local_path" "$remote_path" 
}

function rcp_get(){
    local_path="./$2"
    remote_path="$remote_dir/${1#/}"
    scp "$remote_path" "$local_path"
}

function rcp_help(){
    echo "[usage]"
    echo "rcp send <local_file> [<remote dir>]"
    echo "rcp get <remote_file> [<remote dir>]"
}

while getopts "h" op
do
    if [ "$op" = "h" ] || [ "$op" = "?" ];then
        rcp_help
        exit 0
    fi
done

action="$1"
if [ "$action" = "send" ];then
    rcp_send $2 $3
elif [ "$action" = "get" ];then
    rcp_get $2 $3
else
    echo "unknown action $action"
    rcp_help
    exit 1
fi





