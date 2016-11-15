#!/bin/bash





if [ ($1 == "-h") || ($# -ne 2) ]; then
	echo "Tor Private Network Deploy Script"
	echo "Useage: ./deploy.sh [DA | RELAY | EXIT | CLIENT | HS] [UTIL IP]"
	echo "---------------------------------------------------------------"
	echo "Example: ./deploy.sh DA 172.19.43.32 (For a DA)"
	echo "Example: ./deploy.sh RELAY 172.19.43.32 (For a Relay)"
	echo "\n"
fi


# Delete existing tor on box
echo > /etc/tor/torrc
rm -r /var/lib/tor/keys
rm -r /tor

# Define Variables
ROLE=$1
UTIL_SERVER=$2
TOR_DIR="/var/lib/tor"
TOR_ORPORT=7000
TOR_DIRPORT=9898
TORRC_CONFIG_DIR="/tor/config"


echo -e "\n========================================================"

	
##############################
# Install Build Dependencies #
##############################

echo "[!] Updating package manager"
apt-get update > /dev/null

echo "[!] Installing tor"
apt-get install -y tor > /dev/null

echo "[!] Installing pwgen to generate hostnames"
apt-get install -y pwgen > /dev/null

# See below for comment on git
#echo "[!] Installing git"
#apt-get install -y git > /dev/null

echo "[!] Installing sshpass to auto login with sand ssh"
apt-get install -y sshpass > /dev/null


# Stop tor service
sudo service tor stop
echo "[!] chainging /var/lib/tor permissions to root"
chown root /var/lib/tor

# Changed this so we no longer need to clone the git repo and install git, the repo is pulled once
# when the util box is deployed and the update_torrc_DAs.sh script is moved into the utils apache web root allowing us
# to wget it instead of pull down the entire git repo

wget ${UTIL_SERVER}/update_torrc_DAs.sh -P ${TOR_DIR}/
# Clone github repo
#echo "[!] Cloning GIT Repo"
#git clone https://github.com/98Giraffe/RIT_Capstone_2016.git


# Copying TOR folder from get to /
#cp -r RIT*/tor /


#################################
# Generate torrc common configs #
#################################

# Generate Nickname
RPW=$(pwgen -0A 5)

# Export TOR_NICKNAME environment variable
export TOR_NICKNAME=${ROLE}${RPW}
echo "[!] Setting random Nickname: ${TOR_NICKNAME}"

# Add nickname to torrc
echo -e "\nNickname ${TOR_NICKNAME}" >> /etc/tor/torrc
	
# Add data directory to torrc
echo -e "DataDirectory ${TOR_DIR}" >> /etc/tor/torrc

# Get IP
# get ip using ip command consider editing to use ifconfig if ip addr is not aviable
# Or other tool (kernel files?)
TOR_IP=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1 -d'/')
	
# Add IP to torrc
echo "[!] Setting IP to ${TOR_IP}"
echo "Address ${TOR_IP}" >> /etc/tor/torrc

# Add Control Port to torrc
echo -e "ControlPort 0.0.0.0:9051" >> /etc/tor/torrc

# Add ContactInfo to torrc
echo -e "ContactInfo kar@bar.gov" >> /etc/tor/torrc

# Add TestingTorNetwork to torrc
echo -e "TestingTorNetwork 1" >> /etc/tor/torrc



##############################
# DA Specific Configurations #
##############################

if [ $ROLE == "DA" ]; then

	echo "[!] Setting Role to DA"

	# Append DA template config file to the end of current torrc
	echo "[!] appending DA config to torrc"
	cat ${TORRC_CONFIG_DIR}/torrc.da >> /etc/tor/torrc
	
	# Adding OrPort to torrc
	echo "[!] Opening OrPort ${TOR_ORPORT}"
	echo -e "OrPort ${TOR_ORPORT}" >> /etc/tor/torrc

	# Adding Dirport to torrc
	echo -e "Dirport ${TOR_DIRPORT}" >> /etc/tor/torrc

	# Adding ExitPolicy to torrc
	# check what exit policy shoudl be on dir authority
	echo -e "ExitPolicy accept *:*" >> /etc/tor/torrc

	# Adding V3AuthVotingInterval for lower consensus time from 5 minuets to two
	echo -e "V3AuthVotingInterval 2 minutes" >> /etc/tor/torrc
	
	# Generate Tor path for keys to be stored
	KEYPATH=${TOR_DIR}/keys
	echo "[!] Making Key Path ${KEYPATH}"

	# Make the directory for keys
	mkdir -p ${KEYPATH}

	# Generate Tor Certificates
	echo "[!] Generating Tor Certificates"
	echo "password" | tor-gencert --create-identity-key -m 12 -a ${TOR_IP}:${TOR_DIRPORT} \
	-i ${KEYPATH}/authority_identity_key \
	-s ${KEYPATH}/authority_signing_key \
	-c ${KEYPATH}/authority_certificate \
        --passphrase-fd 0

	# Generate router fingerprint
	echo "[!] Generating Router Fingerprint"
	tor --list-fingerprint --orport 1 \
    	--dirserver "x 127.0.0.1:1 ffffffffffffffffffffffffffffffffffffffff" \
    	--datadirectory ${TOR_DIR}

	# Generate DirAuthority torrc line
	echo "[!] Generating DirAuthority Line"
	AUTH=$(grep fingerprint ${TOR_DIR}/keys/authority_certificate | awk -F " " '{print $2}')
	FING=$(cat $TOR_DIR/fingerprint | awk -F " " '{print $2}')
	SERVICE=$(grep "dir-address" $TOR_DIR/keys/* | awk -F " " '{print $2}')
	
	#echo AUTH ${AUTH}
	#echo FING ${FING}
	#echo SERVICE ${SERVICE}
	#echo IP ${TOR_IP}
	
	TORRC="DirAuthority $TOR_NICKNAME orport=${TOR_ORPORT} no-v2 v3ident=$AUTH $SERVICE $FING"
	
	echo [!] TORRC $TORRC
	echo $TORRC >> /etc/tor/torrc
	echo "[!] Uploading DirAuthoirty torrc config to util server"
	echo $TORRC | sshpass -p "wordpass" ssh -oStrictHostKeyChecking=no tor@$UTIL_SERVER "cat >> ~/DAs"
fi


#################################
# Relay Specific Configurations #
#################################

if [ $ROLE == "RELAY" ]; then

	echo "[!] Setting role to RELAY"
	
	# Set OrPort in torrc
	echo -e "OrPort ${TOR_ORPORT}" >> /etc/tor/torrc
	
	# Set Dirport in torrc
	echo -e "Dirport ${TOR_DIRPORT}" >> /etc/tor/torrc
	
	# Set ExitPolicy in torrc
	echo -e "ExitPolicy accept private:*" >> /etc/tor/torrc

fi

################################
# Exit Specific Configurations               #
################################

if [ $ROLE == "EXIT" ]; then
	
	echo "[!] Setting role to Exit"

	# Set OrPort in torrc
	echo -e "OrPort ${TOR_ORPORT}" >> /etc/tor/torrc
	
	# Set DirPort in torrc
	echo -e "Dirport ${TOR_DIRPORT}" >> /etc/tor/torrc
	
	# Set ExitPolicy in torrc
	echo -e "ExitPolicy accept *:*" >> /etc/tor/torrc
fi

##################################
# Client Specific Configurations #
##################################

if [ $ROLE == "CLIENT" ]; then

	echo "[!] Setting role to Client"
	
	# Set SOCKSPort in torrc
	echo -e "SOCKSPort 0.0.0.0:9050" >> /etc/tor/torrc

fi


################################
# Host Specific Configurations #
################################

if [ $ROLE == "HS" ]; then

	echo "[!] Setting role to Hidden Service"
	
	# Adding HiddenServiceDir to torrc will be located at /var/lib/tor/hs
	echo -e "HiddenServiceDir ${TOR_DIR}/hs" >> /etc/tor/torrc
	TOR_HS_PORT=80
	TOR_HS_ADDR=127.0.0.1
	echo -e "HiddenServicePort ${TOR_HS_PORT} ${TOR_HS_ADDR}:${TOR_HS_PORT}" >> /etc/tor/torrc
	
fi

echo "[!] Creating cron job to update DA entries regurarly"
# Adding update_torrc to cron job
(crontab -l 2>/dev/null; echo "*/1 * * * * ${TOR_DIR}/update_torrc_DAs.sh ${UTIL_SERVER}") | crontab -

echo "[!] Updating DAs list once before cron kicks in"
# Update DAs in torrc
${TOR_DIR}/update_torrc_DAs.sh ${UTIL_SERVER}

# Add update_torrc_DAs.sh as a cron job running every minute
#*/1 * * * * /tor/update_torrc_DAs.sh

echo -e "\n========================================================"
# display Tor version & torrc in log
tor --version
cat /etc/tor/torrc
echo -e "========================================================\n"


tor --RunAsDaemon 1

