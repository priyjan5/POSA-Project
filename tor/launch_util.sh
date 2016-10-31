#!/bin/bash

echo "[!] Updating package manager"
sudo apt-get -y update


echo "[!] installing openssh server"
sudo apt-get install -y openssh-server > /dev/null


useradd tor
passwd tor
usermod -aG sudo tor
