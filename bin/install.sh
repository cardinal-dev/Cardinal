#!/bin/bash

# Cardinal - An Open Source Cisco Wireless Access Point Controller

# MIT License

# Copyright © 2019 Cardinal Contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# This script is designed to configure Cardinal information, such as system variables, system dependencies, etc. 
# If anything needs improvement, please open a pull request on my GitHub! Thanks!

######################################################################
# IMPORTANT: Wipe out the OLD configuration before using this script!#
######################################################################

# First, we need to know some things. How about we start with database (MySQL) information?
echo "Welcome to the Cardinal Initial Configuration Guide!"
echo "MySQL Information"
echo -e ""
read -p "Hello, welcome to Cardinal! What is the hostname/IP address of the database for Cardinal? " dbIP
echo -e ""
read -p "Ok, I got it. How about an username for the database? " dbUsername
echo -e ""
read -p "Great! How about a password for the database? " dbPassword
echo -e ""
read -p "Okay, now we need a name for the database. What is the database name? " dbName
echo -e ""
read -p "Okay, now we need to add a Cardinal Admin. What is the desired username for Cardinal? " cardinalUser
echo -e ""
read -p "Okay, now what is the Cardinal Admin's password? " cardinalPass
echo -e ""
read -p "Finally, where do you want to store your MySQL database information?" dbCredDir
echo -e ""
echo "Cardinal Settings & Configuration"
read -p "Okay, now we need a directory where Cisco IOS images reside. Where is this directory at? " tftpDir
echo -e ""
read -p "Okay, now we need a duration (in minutes) when Cardinal will pull info from access points (e.g. clients associated, bandwidth, etc.) What is the desired duration in minutes? " schedulePoll
echo -e ""
read -p "Okay, now we need the base location of your Cardinal installation. What is the absolute path of your Cardinal installation? " cardinalBase
echo "Thank you for installing Cardinal!"

# Let's create a system user called cardinal. The cardinal user is the user which will run our processes
sudo adduser cardinal

# Let's create a configuration file based on user input (for Cardinal SQL connections)
rm $dbCredDir/cardinal.ini
touch $dbCredDir/cardinal.ini
echo "[cardinal]" >> $dbCredDir/cardinal.ini
echo 'dbserver'=""$dbIP"" >> $dbCredDir/cardinal.ini
echo 'dbuser'=""$dbUsername"" >> $dbCredDir/cardinal.ini
echo 'dbpassword'=""$dbPassword"" >> $dbCredDir/cardinal.ini
echo 'dbname'=""$dbName"" >> $dbCredDir/cardinal.ini
echo 'commanddir'="<COMMAND_DIR_HERE>" >> $dbCredDir/cardinal.ini

# Let's create a log file for Cardinal UI
mkdir -p /var/log/cardinal
chown -R cardinal:cardinal /var/log/cardinal
touch /var/log/cardinal/cardinal.log

# Generate Cardinal venv
sudo python3 -m venv $cardinalBase/bin/cardinal
sudo $cardinalBase/bin/cardinal/pip install -r $cardinalBase/requirements.txt

# Let's create a socket directory for uWSGI
mkdir -p /var/lib/cardinal
chown -R cardinal:cardinal /var/lib/cardinal

# Set permissions on the cardinal.ini file
chown -R cardinal:cardinal $dbCredDir/cardinal.ini

# Now, let's create the MySQL database for Cardinal. We also want to import the SQL structure too!
mysql -u$dbUsername -p$dbPassword -e "CREATE DATABASE "$dbName""
mysql -u$dbUsername --password=$dbPassword $dbName < ../sql/cardinal.sql

# Add Cardinal configuration to MySQL
mysql -u$dbUsername -p$dbPassword $dbName -e "INSERT INTO settings (settings_id,cardinal_tftp,poll_schedule) VALUES ('1','$tftpDir','$schedulePoll')"

# Now, let's create a Cardinal admin
hashedPass=$(python3 -c 'from werkzeug.security import generate_password_hash; print(generate_password_hash("'$cardinalPass'", "sha256"))')
mysql -u$dbUsername -p$dbPassword $dbName -e "INSERT INTO users (username,password) VALUES ('$cardinalUser','$hashedPass')"
