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
echo "For more information, please visit http://cardinal.mcclunetechnologies.net"
echo "MySQL Information"
echo -e ""
read -p "Hello, welcome to Cardinal! What is the hostname/IP address of the database for Cardinal? " varDatabaseIP
echo -e ""
read -p "Ok, I got it. How about an username for the database? " varDbUsername
echo -e ""
read -p "Great! How about a password for the database? " varDbPassword
echo -e ""
read -p "Okay, now we need a name for the database. What is the database name? " varDbName
echo -e ""
read -p "Okay, now we need to add a Cardinal Admin. What is the desired username for Cardinal? " varCardinalUser
echo -e ""
read -p "Okay, now what is the Cardinal Admin's password? " varCardinalPass
echo -e ""
read -p "Finally, where do you want to store your MySQL database information? REMEMBER: This location shouldn't be the web root, this should be a directory outside of the web root. Please make sure you give www-data or your web server rights to read the file. " varDbCredDir
echo -e ""
echo "Cardinal Settings & Configuration"
read -p "Okay, now we need a directory where Cisco IOS images reside. Where is this directory at? " varTftpDir
echo -e ""
read -p "Okay, now we need a duration (in minutes) when Cardinal will pull info from access points (e.g. clients associated, bandwidth, etc.) What is the desired duration in minutes? " varSchedulePoll
echo -e ""
read -p "Okay, now we need the base location of your Cardinal installation. What is the absolute path of your Cardinal installation? " varCardinalBase
echo "Thank you for installing Cardinal!"

# Let's create a configuration file based on user input (for Cardinal SQL connections)
rm $varDbCredDir/cardinal.ini
touch $varDbCredDir/cardinal.ini
echo "[cardinal_config]" >> $varDbCredDir/cardinal.ini
echo 'dbserver'=""$varDatabaseIP"" >> $varDbCredDir/cardinal.ini
echo 'username'=""$varDbUsername"" >> $varDbCredDir/cardinal.ini
echo 'password'=""$varDbPassword"" >> $varDbCredDir/cardinal.ini
echo 'dbname'=""$varDbName"" >> $varDbCredDir/cardinal.ini

# Now, let's create the MySQL database for Cardinal. We also want to import the SQL structure too!
mysql -u$varDbUsername -p$varDbPassword -e "CREATE DATABASE "$varDbName""
mysql -u$varDbUsername --password=$varDbPassword $varDbName < ../sql/cardinal.sql

# Add Cardinal configuration to MySQL
mysql -u$varDbUsername -p$varDbPassword $varDbName -e "INSERT INTO settings (settings_id,cardinal_home,cardinal_tftp,poll_schedule) VALUES ('1','$varConfigDir','$varTftpDir','$varSchedulePoll')"

# Now, let's create a Cardinal admin
hashedPass=$(python3 -c 'from werkzeug.security import generate_password_hash; print(generate_password_hash("'$varCardinalPass'", "sha256"))')
mysql -u$varDbUsername -p$varDbPassword $varDbName -e "INSERT INTO users (username,password) VALUES ('$varCardinalUser','$hashedPass')"
