#!/bin/bash

# Travis-CI Builder
# falcon78921

# For Travis-CI Builds
sudo rm /var/lib/apt/lists/lock
sudo rm /var/cache/apt/archives/lock
sudo rm /var/lib/dpkg/lock

# Add ppa:ondrej/php as source for Ubuntu & update sources
sudo apt-get install -y software-properties-common
sudo apt-get install -y python-software-properties
sudo add-apt-repository -y ppa:ondrej/php
sudo apt-get update

# Install Dependencies
sudo apt-get install openssh-server openssh-client mysql-server mysql-client git apache2 python-paramiko python php7.0 php7.0-mysql snmp nmap curl traceroute whois tftpd-hpa
