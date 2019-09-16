#!/bin/bash

KEY=$(cat key.txt)
FILE_IN=flag.txt
FILE_OUT=flag.enc

./Basement.exe "encrypt" "$KEY" "$FILE_IN" "$FILE_OUT"
