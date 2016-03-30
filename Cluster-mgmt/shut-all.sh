#! /bin/bash

for SLAVE in $(cat slaves.txt);
do
    ssh $SLAVE shutdown -h -P now;
done
