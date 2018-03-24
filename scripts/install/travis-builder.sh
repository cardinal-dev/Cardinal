#!/bin/bash

# Travis-CI Builder
# falcon78921

# Add ppa:ondrej/php as source for Ubuntu & update sources
sudo apt-get install -y software-properties-common
sudo apt-get install -y python-software-properties
sudo add-apt-repository -y ppa:ondrej/php
sudo apt-get update

# Install MySQL Server
sudo apt-get purge mysql-client-core-5.6
sudo apt-get autoremove
sudo apt-get autoclean
sudo apt install mysql-client-core-5.5
sudo apt install mysql-server

# Install Dependencies
sudo apt-get install openssh-server openssh-client git apache2 python-paramiko python php7.0 php7.0-mysql snmp nmap curl traceroute whois tftpd-hpa
