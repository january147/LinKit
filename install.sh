#!/bin/bash
# Date: Sat Jul 13 17:32:55 2019
# Author: 

set -e

# 双引号“”会抑制波浪线～展开成主目录！！！
DES_DIR=~/bin
ORG_DIR=./bin
UNINSTALL_MANIFEST=LinKit.manifest
force_install=no

# 是否忽略同名文件
if [ $# -gt 0 ] && [ $1 == -f ]; then
    force_install=yes
fi

# 检查清单文件
if [ -e $DES_DIR/$UNINSTALL_MANIFEST ]; then
    echo -n "$DES_DIR/$UNINSTALL_MANIFEST exists, "
        if [ $force_install == no ]; then
            echo "aborting..."
            exit -1
        else
            echo "deleting..."
            rm $DES_DIR/$UNINSTALL_MANIFEST
        fi
fi

# do必须换行！！！
for file in $(ls ./bin) 
do
    new_name=${file%.*}
    # 判断文件是否存在
    if [ -e $DES_DIR/$new_name ]; then
        echo -n "$DES_DIR/$new_name exists, "
        if [ $force_install == no ]; then
            echo "aborting..."
            exit -1
        else
            echo "overwriting..."
        fi
    fi
    
    if [ -d $ORG_DIR/$file ]; then
        cp -r $ORG_DIR/$file $DES_DIR/$file
    else
        cp $ORG_DIR/$file $DES_DIR/$new_name
    fi
    echo $DES_DIR/$new_name >> $DES_DIR/$UNINSTALL_MANIFEST
done

# 把安装清单文件文件名加入清单文件中
echo $DES_DIR/$UNINSTALL_MANIFEST >> $DES_DIR/$UNINSTALL_MANIFEST
# 放置卸载脚本
cp uninstall.sh $DES_DIR/uninstall
