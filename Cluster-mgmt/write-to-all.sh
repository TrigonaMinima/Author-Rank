#! /bin/bash

fileto=$1
text=$2

for SLAVE in $(cat slaves.txt);
do
    echo $text | ssh $SLAVE "cat >> $fileto";
done
