#! /bin/bash

for SLAVE in $(cat slaves.txt);
do
    echo $SLAVE;
    ssh -t $SLAVE sudo shutdown -h now;
done
