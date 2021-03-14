#!/bin/bash

python edit_configs.py --lang
python edit_configs.py --show
rm -rf public/events
cpp -R events public

build='build'
if [ $# -ge 1 ]; then
    build=$1
fi

npm run $build

checkyes "scp to lab?"
if [ $? -eq 0 ]; then
    checkyes "make a backup at lab:~/public_backup ?"
    if [ $? -eq 0 ]; then
        ssh lab cp -r ~/public_html ~/public_backup
    fi
    # scp -rp dist/* lab:~/public_test
fi
