#!/usr/bin/bash

log_path=/var/log/app

result=$(find ${log_path}/*.log -type f)
files=($result)

for file in "${files[@]}"
do
    date=$(date +"%Y%m%d%H%M%S")
    mv ${file} ${file}_${date}
    # or do whatever with individual element of the array
done

find ${log_path}/*.log* -type f -mtime +30 -delete
