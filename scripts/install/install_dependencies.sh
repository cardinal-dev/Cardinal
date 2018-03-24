#!/bin/bash

# Install Cardinal Dependencies
# falcon78921

# Add ppa:ondrej/php as source for Ubuntu & update sources
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update

# Install Dependencies
apt-get install openssh-server openssh-client mysql-server mysql-client git apache2 python-paramiko python php7.0 php7.0-mysql snmp nmap curl traceroute whois tftpd-hpa
