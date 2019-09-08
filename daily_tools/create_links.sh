#!/bin/bash
# Date: Thu May  9 11:54:37 2019
# Author: January

# 测试是否有abspath
abspath >> /dev/null 2>&1

if [ $? -eq 0 ]; then
    while [[ $# -gt 0 ]]; do
        tmp=${1##*/}
        file=${tmp%.*}
        abspath=`abspath "$1"`
        ln -s "$abspath" "$file"
        echo $file
        shift
    done
else
    echo "abspath not install, aborting..."
    exit -1
fi

