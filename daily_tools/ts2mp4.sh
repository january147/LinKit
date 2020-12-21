#!/bin/bash
# Date: Wed Feb  5 17:03:56 2020
# Author: January

set -o errexit

function ts2mp4_help(){
    echo "This tool is used to merge mpegts files into a complete mp4"
    echo "ts2mp4 <video_pieces_dir> <output_filename>"
}

if [ "$1" == "-h" ];then
    ts2mp4_help
    exit 0
fi

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
