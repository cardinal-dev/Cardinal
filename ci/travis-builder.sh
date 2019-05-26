#!/bin/bash

# Travis-CI Builder
# falcon78921

# Install dependencies
sudo apt-get install -y openssh-server openssh-client git apache2 snmp nmap curl traceroute whois tftpd-hpa python3-setuptools python3-pip python3
sudo pip3 install paramiko pyinstaller

# Add Python testing
sudo apt-get install -y pyflakes3
