#!/bin/bash

# Travis-CI Builder
# falcon78921

# Add ppa:ondrej/php as source for Ubuntu & update sources
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:ondrej/php
sudo apt-get update

# Install dependencies
sudo apt-get install -y openssh-server openssh-client git apache2 python3-paramiko python3 php7.0 php7.0-mysql snmp nmap curl traceroute whois tftpd-hpa python3-setuptools python3-pip

# Add Python testing
sudo apt-get install -y python3-pyflakes
