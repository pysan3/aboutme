#!/bin/bash

python edit_configs.py --show
python edit_configs.py --lang
rm -rf public/events
cpp -R events public

build='build'
if [ $# -ge 1 ]; then
    build=$1
fi

npm run $build

checkyes "scp to lab?"
if [ $? -eq 0 ]; then
    scp -rp dist/* lab:~/public_test
fi

checkyes 'update webpage?'
if [ $? -eq 0 ]; then
    ssh -t lab:~/hp_update.sh
fi
