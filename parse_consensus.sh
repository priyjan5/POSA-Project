#!/bin/bash
rm ./consensus
#wget http://172.16.106.170:9898/tor/status-vote/current/consensus > /dev/null
wget http://171.25.193.9:443/tor/status-vote/current/consensus
awk -f awk_consesnus.awk ./consensus
