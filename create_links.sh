#!/bin/bash
# Date: Thu May  9 11:54:37 2019
# Author: January

while [[ $# -gt 0 ]]; do
    tmp=${1##*/}
    file=${tmp%.*}
    abspath=`abspath "$1"`
    ln -s "$abspath" "$file"
    echo $file
    shift
done

