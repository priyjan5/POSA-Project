#!/bin/bash

echo "[!] Updating package manager"
sudo apt-get -y update


echo "[!] installing openssh server"
sudo apt-get install -y openssh-server > /dev/null

echo "[!] installing apache2"
sudo apt-get install -y apache2 > /dev/null

echo "[!] installing git"
sudo apt-get install -y git > /dev/null

echo "[!] cloning Capstone Repo"
git clone https://github.com/98Giraffe/RIT_Capstone_2016.git

echo "[!] Copying deploy.sh to apache root"
cp RIT_Capstone_2016/tor/deploy.sh /var/www/html/
cp RIT_Capstone_2016/tor/update_torrc_DAs.sh /var/www/html/

useradd tor
echo tor:wordpass | chpasswd tor
usermod -aG sudo tor

cd /home/tor
touch DAs
chown tor DAs
chgrp tor DAs
