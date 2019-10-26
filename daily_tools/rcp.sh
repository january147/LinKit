#!/bin/bash
# Date: Sat Oct 26 21:12:19 2019
# Author: January

set -o errexit

remote_path="root@39.108.170.44:/root/store"

local_path="$1"
remote_path="$remote_path/${2#/}"
scp "$local_path" "$remote_path" 

