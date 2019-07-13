#!/bin/bash
# Date: Sat Jul 13 18:20:59 2019
# Author: January
UNINSTALL_MANIFEST=LinKit.manifest

for file in $(cat $UNINSTALL_MANIFEST) 
do
    if [ -d $file ]; then
        rm -r $file
    else
        rm $file
    fi
done
rm uninstall