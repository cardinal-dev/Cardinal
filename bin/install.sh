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

# Gather information
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
read -p "Where do you want to store your MySQL database information? " dbCredDir
echo -e ""
read -p "Where is the location of the scout command directory? " commandDir
echo -e ""
read -p "What is the desired Flask key? (i.e. Securing session data) " flaskKey

# Create a system user called cardinal. The cardinal user is the user which will run our processes
sudo useradd cardinal

# Create a log file for Cardinal UI
rm -rf /var/log/cardinal
mkdir -p /var/log/cardinal
touch /var/log/cardinal/cardinal.log
chown -R cardinal:cardinal /var/log/cardinal

# Generate Cardinal venv
sudo python3 -m venv cardinal
sudo cardinal/bin/pip install -U pip
sudo cardinal/bin/pip install -r ../requirements.txt
sudo cardinal/bin/pip install ../lib/.

# Create a socket directory for uWSGI
rm -rf /var/lib/cardinal
mkdir -p /var/lib/cardinal
chown -R cardinal:cardinal /var/lib/cardinal

# Set permissions on the cardinal.ini file
chown -R cardinal:cardinal $dbCredDir/cardinal.ini

# Create the MySQL database for Cardinal. We also want to import the SQL structure too!
mysql -u$dbUsername -p$dbPassword -e "CREATE DATABASE "$dbName""
mysql -u$dbUsername --password=$dbPassword $dbName < ../sql/cardinal.sql
mysql -u$dbUsername --password=$dbPassword mysql -e "update user set plugin='mysql_native_password' where User='root'"
mysql -u$dbUsername --password=$dbPassword mysql -e "update user set authentication_string=password('$dbPassword') where user='root'"
systemctl restart mysql

# Create a Cardinal admin
hashedPass=$(/opt/Cardinal/bin/cardinal/bin/python -c 'from werkzeug.security import generate_password_hash; print(generate_password_hash("'$cardinalPass'", "sha256"))')
mysql -u$dbUsername -p$dbPassword $dbName -e "INSERT INTO users (username,password) VALUES ('$cardinalUser','$hashedPass')"

# Generate encryption key
encryptKey=$(/opt/Cardinal/bin/cardinal/bin/python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

# Create a configuration file based on user input
rm $dbCredDir/cardinal.ini
touch $dbCredDir/cardinal.ini
echo "[cardinal]" >> $dbCredDir/cardinal.ini
echo 'dbserver'=""$dbIP"" >> $dbCredDir/cardinal.ini
echo 'dbuser'=""$dbUsername"" >> $dbCredDir/cardinal.ini
echo 'dbpassword'=""$dbPassword"" >> $dbCredDir/cardinal.ini
echo 'dbname'=""$dbName"" >> $dbCredDir/cardinal.ini
echo 'commanddir'=""$commandDir"" >> $dbCredDir/cardinal.ini
echo 'flaskkey'=""$flaskKey"" >> $dbCredDir/cardinal.ini
echo 'encryptkey'=""$encryptKey"" >> $dbCredDir/cardinal.ini
echo 'commanddebug=off' >> $dbCredDir/cardinal.ini
