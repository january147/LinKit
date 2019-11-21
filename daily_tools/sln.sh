#!/bin/bash
# Date: Thu May  9 11:54:37 2019
# Author: January

# 测试是否有abspath
abspath >> /dev/null 2>&1

#################config###############
keep_suffix=true
################end config############

function sln_help(){
    echo "This tool is used to create soft links"
    echo "sln <filename>"
    echo "Note:<filename> can be multiple or wildcards"
}

while getopts "h" op
do
    if [ "$op" = "h" ] || [ "$op" = "?" ];then
        sln_help
        exit 0
    fi
done

if [ $? -eq 0 ]; then
    while [[ $# -gt 0 ]]; do
        # 删除目录部分，留下文件名(##是从前面最大匹配后截除)
        tmp=${1##*/}
        # 删除文件后缀名部分
        if [ $keep_suffix = "false" ];then
            file=${tmp%.*}
        else
            file=$tmp
        fi
        # 如果存在同名文件则改名称
        if [ -e "$file" ];then
            file="link_$file"
        fi
        # 获取绝对路径，使得即使链接文件移动仍然可用
        abspath=`abspath "$1"`
        ln -s "$abspath" "$file"
        echo $file
        shift
    done
else
    echo "abspath not install, aborting..."
    exit -1
fi

