#! /bin/bash
slaves=(ap51 ap49 ap56 ap48 ap53 ap47 ap54 ap43 ap55)
for slave in slaves;
do
	ssh $host shutdown -h -P now;
done
