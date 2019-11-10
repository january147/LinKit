#!/bin/bash
# Date: Thu May  9 11:54:37 2019
# Author: January

# 测试是否有abspath
abspath >> /dev/null 2>&1

if [ $? -eq 0 ]; then
    while [[ $# -gt 0 ]]; do
        # 删除目录部分，留下文件名(##是从前面最大匹配后截除)
        tmp=${1##*/}
        # 删除文件后缀名部分
        file=${tmp%.*}
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

