UTIL_SERVER=172.16.106.158
sshpass -p "wordpass" scp -oStrictHostKeyChecking=no tor@${UTIL_SERVER}:~/DAs .

FLAG=0
while read p; do
  	
	cat /etc/tor/torrc | grep "${p}"
	if [ $? != 0 ]; then
		echo "Adding line $p"
		echo $p >> /etc/tor/torrc
		$FLAG=1
	fi
done <./DAs

if [ $FLAG ]; then
	service tor restart
fi

