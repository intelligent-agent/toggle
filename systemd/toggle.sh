#!/bin/sh

case $1 in 
	start)
		export LD_LIBRARY_PATH=/usr/local/lib
		cd /usr/src/toggle/c/ && ./toggle
		echo "Toggle started ok"
		exit 0
		;;
	stop)
		pkill -9 -f toggle
		echo "Execed killall toggle"
		;;
	*)
		echo "Usage: $0 {start|stop}"
esac
