#!/bin/bash
# Date: Sat Jul 13 17:32:55 2019
# Author: January

#####################################################
# 该脚本用于将文件复制到对应目录, 并记录所复制的文件用于删除 #
#####################################################

# 命令运行错误时停止运行
set -e

# !!!双引号“”会抑制波浪线～展开成主目录
# 这里是需要到的目标文件夹，按需调整
DES_DIR=~/bin
# 这里是源文件夹，一般不需要调整
ORG_DIR=./daily_tools
# 记录安装清单文件, 按需修改
UNINSTALL_MANIFEST=LinKit.manifest
# 默认是否覆盖已存在文件(n为否, y为是)
force_install=n
# 安装时是否保留文件扩展名
keep_file_ext=n

# ############询问是否保留文件扩展名，按需启用##################
# echo -n "是否保留文件扩展名？(n) "
# read keep_file_ext
# # 比较符号两边需要加上空格！！!
# if [ -z "$keep_file_ext" ] || [ $keep_file_ext != y -a $keep_file_ext != n ]; then
#     keep_file_ext=n
# fi
# ############询问是否保留文件扩展名##################

# 是否忽略同名文件
if [ $# -gt 0 ] && [ $1 == -f ]; then
    force_install=yes
fi

# 检查清单文件是否存在
if [ -e $DES_DIR/$UNINSTALL_MANIFEST ]; then
    echo -n "$DES_DIR/$UNINSTALL_MANIFEST exists, "
        if [ $force_install == n ]; then
            echo "aborting..."
            exit -1
        else
            echo "deleting..."
            rm $DES_DIR/$UNINSTALL_MANIFEST
        fi
fi

# do必须换行！！！
for file in $(ls $ORG_DIR) 
do
    if [ $keep_file_ext == n ]; then
        new_name=${file%.*}
    else
        new_name=$file
    fi
    # 判断文件是否存在
    if [ -e $DES_DIR/$new_name ]; then
        echo -n "$DES_DIR/$new_name exists, "
        if [ $force_install == n ]; then
            echo "aborting..."
            echo "check $DES_DIR/$UNINSTALL_MANIFEST for successfully installed file"
            exit -1
        else
            echo "overwriting..."
        fi
    fi
    
    if [ -d $ORG_DIR/$file ]; then
        cp -r $ORG_DIR/$file $DES_DIR/
    else
        cp $ORG_DIR/$file $DES_DIR/$new_name
    fi
    # 每复制一个文件,就将其记录在清单文件中
    echo $DES_DIR/$new_name >> $DES_DIR/$UNINSTALL_MANIFEST
done

# 把安装清单文件文件名加入清单文件中
echo $DES_DIR/$UNINSTALL_MANIFEST >> $DES_DIR/$UNINSTALL_MANIFEST

# 测试是否有卸载脚本同名文件
if [ -e $DES_DIR/uninstall ]; then
    echo -n "uninstall exists, "
    if [ $force_install == n ]; then
        echo "aborting..."
        echo "check $DES_DIR/$UNINSTALL_MANIFEST for successfully installed file"
        exit -1
    else
        echo "overwriting..."
    fi
fi
cp uninstall.sh $DES_DIR/uninstall
