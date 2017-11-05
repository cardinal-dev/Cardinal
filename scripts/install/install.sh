#!/bin/bash

# Cardinal Install Script
# falcon78921

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
echo "Nice! For security, please run this command after you are done configuring Cardinal: cat /dev/null > ~/.bash_history"
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
read -p "Okay, now we need a directory where the Cardinal configuration will reside. Where is this directory at? " varConfigDir
echo -e ""
read -p "Okay, now we need a directory where the Cardinal scripts will reside. Preferably, this should be OUTSIDE of the web root. What is the directory? " varDirScripts
echo -e ""
read -p "Okay, now we need the base location of your Cardinal installation. What is the absolute path of your Cardinal installation? " varCardinalBase
echo "Thank you for installing Cardinal!"

# Let's create a php_cardinal.php configuration file based on user input (for Cardinal SQL connections)
touch $varDbCredDir/php_cardinal.ini
echo "[cardinal_mysql_config]" >> $varDbCredDir/php_cardinal.ini
echo 'servername'=""$varDatabaseIP"" >> $varDbCredDir/php_cardinal.ini
echo 'username'=""$varDbUsername"" >> $varDbCredDir/php_cardinal.ini
echo 'password'=""$varDbPassword"" >> $varDbCredDir/php_cardinal.ini
echo 'dbname'=""$varDbName"" >> $varDbCredDir/php_cardinal.ini

# Let's then create a configuration file (for other Cardinal stuff)
touch $varConfigDir/cardinal_config.ini
echo "[cardinal_config]" >> $varConfigDir/cardinal_config.ini
echo 'scriptsdir'=""$varDirScripts"" >> $varConfigDir/cardinal_config.ini
echo 'cardinalbase'=""$varCardinalBase"" >> $varConfigDir/cardinal_config.ini

# Let's also give the non-web directory Apache read rights
chown -R www-data:www-data $varDbCredDir
chown -R www-data:www-data $varConfigDir
chown -R www-data:www-data $varDirScripts

# Now, let's create the MySQL database for Cardinal. We also want to import the SQL structure too!
mysql -u$varDbUsername -p$varDbPassword -e "CREATE DATABASE "$varDbName""
mysql -u$varDbUsername --password=$varDbPassword $varDbName < $varCardinalBase/sql/cardinal.sql

# Now, let's create a Cardinal admin
hashedPass=$(python -c 'import crypt; print crypt.crypt("'$varCardinalPass'", "$6$random_salt")')
mysql -u$varDbUsername -p$varDbPassword $varDbName -e "INSERT INTO users (username,password) VALUES ('$varCardinalUser','$hashedPass')"

# Add fetch_all_clients.php to crontab (for constant pull of all AP clients)
crontab -l > fetch_all_clients
echo "* * * * * php" $varDirScripts"/fetch_all_clients.php" >> fetch_all_clients
crontab fetch_all_clients
rm fetch_all_clients
