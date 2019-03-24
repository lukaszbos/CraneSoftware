#!/bin/bash

echo "Script started"

#mkfifo pipe

#arg

#./yoloScript.sh < pipe | (python3 pad.py) > pipe

#rm pipe

#> test.txt

python3 ../padfiles/pad.py

clear

#pads=(python3 pad.py)

#cat $pads >> test.txt
