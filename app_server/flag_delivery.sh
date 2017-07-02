#!/bin/bash

delivery(){
	for i in `ls /home/`
	do
		if [ "${i:(-1)}" == "${1:(-1)}" ]
		then
			cp "/home/ftp_user/ftp/files/$1" "/home/$i/flag.txt"
			chown $i:$i "/home/$i/flag.txt"
			chmod 400 "/home/$i/flag.txt"
		fi
	done
}

monitor(){
	MonitorDir="/home/ftp_user/ftp/files/"
	inotifywait -m -r -e modify --format '%w%f' "${MonitorDir}" | while read MODIFY
	do
		for i in `ls /home/ftp_user/ftp/files/`
		do
			delivery "$i"
		done
	done
}

monitor &
