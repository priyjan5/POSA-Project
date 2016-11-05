UTIL_SERVER=172.16.106.158
sshpass -p "wordpass" scp tor@${UTIL_SERVER}:~/DAs .

while read p; do
  
	cat /etc/tor/torrc | grep "${p}"
	if [ $? == 1 ]; then
		echo "Adding line $p"
		echo $p >> /etc/tor/torrc
	fi

done <./DAs
