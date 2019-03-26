#!/bin/bash

printf ">>> Script started <<< \n\n"

# g++ -o testStreamLoader testStreamLoader.cpp

#python3 ../padfiles/pad.py | ./testStreamLoader
file1=$1
file2=$2

fileCheck() {
  if [ -f $1 ]; then
    printf ">> $1 << Ideed exists \n"
  else
    printf ">> $1 << Does not exist! \nProgram aborted \n" >&2
    exit 125
  fi
}

get_starter() {
  a=$1
  if grep -q "." "$a"; then
  b=${a##*.}
  # echo $b
    if [[ $b == "py" ]]; then
      echo "python3 "
    fi
    if [[ $b == "sh" ]]; then
      printf "./"
    fi
    if [[ $b == "jar" ]]; then
      printf "java -jar  "
    fi
  else
    printf ./
  fi
}

if [[ $# -lt 2 ]]; then
  printf "Not enough arguments. Correct syntax is: \n   ./run.sh <output_file> <input_file>"
  sleep 1s
  # python3 padfiles/pad.py | ./linuxScripts/testStreamLoader
fi
if [[ $# -ge 2 ]]; then
  (fileCheck $file1)
  (fileCheck $file2)
  starter_1=$(get_starter $file1)
  starter_2=$(get_starter $file2)

  echo ${file1#*.}

  echo $starter_1 $starter_2
  $starter_1$file1 | $starter_2$file2

fi
