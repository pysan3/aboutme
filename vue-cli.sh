#!/bin/bash

python edit_configs.py --lang
python edit_configs.py --show
\rm -rf public/events
cpp -R events public

if [[ x"$1" = xserve ]]; then
    npm run "$1"
    return
fi

npm run $1

checkyes "scp to lab?"
if [ $? -eq 0 ]; then
    checkyes "make a backup at lab:~/public_backup ?"
    if [ $? -eq 0 ]; then
        ssh lab cp -r ~/public_html ~/public_backup
    fi
    rsync -rp dist/* lab:~/public_html
fi

checkyes "scp to nginx?"
if [ $? -eq 0 ]; then
    ssh dynabook mkdir -p /var/www/html/~takuto
    rsync -r dist/* dynabook:/var/www/html/~takuto
fi
