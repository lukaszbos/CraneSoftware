#!/bin/bash

printf ">>> Script started <<<"

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
  if [[ $1 == "*.*" ]]; then
    a=$1
    b=${a#*.}
    if [[ $b == "sh" ]]; then
      printf ./
    fi
    if [[ $b == "py" ]]; then
      printf "python3 "
    fi
  fi
  if [[ $1 != "*.*" ]]; then
    printf ./
  fi
}

if [[ $# -lt 2 ]]; then
  printf "Not enough arguments. Script is runnig default programs"
  sleep 5s
  python3 ../padfiles/pad.py | ./testStreamLoader
fi
if [[ $# -ge 2 ]]; then
  (fileCheck $file1)
  (fileCheck $file2)
  starter_1=$(get_starter $file1)
  starter_2=$(get_starter $file2)

  echo $starter_1 $starter_2
  $starter_1$file1 | $starter_2$file2

fi
