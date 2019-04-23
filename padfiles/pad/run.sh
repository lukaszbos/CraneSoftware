#!/bin/bash

echo "Script started"

mkfifo pipe

#arg

./yoloScript.sh < pipe | (python3 pad.py) > pipe

rm pipe

#> test.txt

#pads=(python3 pad.py)

#cat $pads >> test.txt
