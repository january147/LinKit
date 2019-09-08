#!/bin/bash
# Date: Sat Jul 13 18:20:59 2019
# Author: January

#####################################
# 该脚本根据清单文件删除本目录下的对应文件 #
#####################################

set -e
# 记录需要卸载文件的清单文件名
UNINSTALL_MANIFEST=LinKit.manifest

for file in $(cat $UNINSTALL_MANIFEST) 
do
    if [ -d $file ]; then
        rm -r $file
    elif [ -e $file ]; then
        rm $file
    fi
done
rm uninstall