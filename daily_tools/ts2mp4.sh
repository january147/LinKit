#!/bin/bash
# Date: Wed Feb  5 17:03:56 2020
# Author: January

set -o errexit

dir=$1
des_path=$2
# check parameter
if [ -z "$dir" ]; then
    dir="."
fi

if [ -z "$des_file" ]; then
    des_path="video.mp4"
fi

cd $dir
# backup m3u8 files
for file in $(ls *.m3u8)
do
    if [ ! -e $file.bak ];then
        cp $file $file.bak
    fi
done

sed -i "s/\///g" *.m3u8
ffmpeg -allowed_extensions ALL -i index.m3u8 -c copy $des_path
