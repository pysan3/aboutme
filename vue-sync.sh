#!/bin/bash

FILE=src/views/$(ls --color=auto src/views | grep $1)
file=`echo $1 | awk '{print tolower($0)}'`

BASE="
Codes
Datasets
Papers
Researches
"

while IFS= read -r f; do
    out="src/views/$f.vue"
    lower=`echo "$f" | awk '{print tolower($0)}'`
    if [ -f "$out" ] && [ "$f".vue != `basename "$FILE"` ]; then
        diff "$out" "$FILE"

        echo "Overwriting $out with $FILE"
        checkyes 'Ok?'
        echo $?
        if [ $? -eq 0 ]; then
            cp "$FILE" "$out"
            sed -i "s/$file/$lower/g" "$out"
        fi
    fi
done <<< "$BASE"

