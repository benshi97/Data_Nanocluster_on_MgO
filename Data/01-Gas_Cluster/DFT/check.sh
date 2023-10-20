#!/bin/bash

find . -type d | while read -r dir; do
    if [[ ! -e "$dir/OUTCAR" ]]; then
        echo "$dir does not contain OUTCAR"
    fi
done

