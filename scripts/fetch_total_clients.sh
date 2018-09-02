#!/bin/bash

# Cardinal Fetch Total Number of Clients Associated
# falcon78921

# After we have queried the SQL database, launched the associations command
# via SSH, and received the output.

# Cardinal Configuration Variable Declarations

# IMPORTANT!: Modify this to include the proper location of the scripts directory
mysqlAuth=$(awk -F "=" '/scriptsdir/ {print $2}' /path/to/cardinalmysql.ini)

# Get values from MySQL database
scriptsDir=$(echo "SELECT cardinalScripts FROM settings WHERE settings_id = 1" | mysql $dbname -u $username -p$password)
echo $scriptsDir

# Open Connection to Each AP in Cardinal Database
mkdir $scriptsDir/results
python $scriptsDir/cisco_count_clients.py $1 $2 $3 $4 > $scriptsDir/results/$4.results

# Run grep query, specifically for MAC addresses that were collected from PHP script

grep -o "[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f]" $scriptsDir/results/$4.results > $scriptsDir/results/$4.macs.txt

# Run line count to get exact amount of clients associated, for each access point. Remove excess files.

rm -r $scriptsDir/results/*.results
wc -l < $scriptsDir/results/$4.macs.txt > $scriptsDir/results/$4.clients

# Remove excess files. There you go!

rm -r $scriptsDir/results/*.macs.txt

# Rinse & Repeat!
