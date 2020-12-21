#!/bin/bash
# Date: Mon Dec 21 15:58:39 2020
# Author: January

if [ -d "$1" ];then
    cd $1
    pwd
elif [ -e "$1" ];then
    filename=${1##*/}
    dir=${1%/*}
    if [ -n "$dir" ];then
        cd $dir
    fi
    echo "$(pwd)/$filename"
elif [ -z "$1" ];then
    pwd
else
    echo "No such file or directory"
fi