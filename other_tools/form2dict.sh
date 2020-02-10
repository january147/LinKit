#!/bin/bash
# Date: Sun Feb  9 18:07:15 2020
# Author: January

# 其中\1和\2分别代表匹配项中的第一个和第二个组的原内容

cat | sed -e "s/&/\n,/g" | sed "s/\(.*\)=\(.*\)/\"\1\" : \"\2\"/g"