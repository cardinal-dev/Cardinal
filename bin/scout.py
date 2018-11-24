#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2017 falcon78921

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import paramiko
import time
import sys
import subprocess
import mysql.connector
from ConfigParser import SafeConfigParser

# Connect to MySQL database

mysqlConfig = SafeConfigParser()
mysqlConfig.read("/path/to/cardinalmysql.ini")
mysqlHost = mysqlConfig.get('cardinal_mysql_config', 'servername')
mysqlUser = mysqlConfig.get('cardinal_mysql_config', 'username')
mysqlPass = mysqlConfig.get('cardinal_mysql_config', 'password')
mysqlDb = mysqlConfig.get('cardinal_mysql_config', 'dbname')

conn = mysql.connector.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPass, db = mysqlDb)

# Variable declarations

queryCommand = sys.argv[1]

# Scout help & usage

if queryCommand == "--help":
   print("Scout: Cardinal CLI for managing Cisco access points")
   print("Usage:")
   print("   scout.py --get-arp: print access point ARP table")
   print("   scout.py --led: trigger LED function for 30 seconds")
   print("   scout.py --change-ip: change access point IP")
   print("   scout.py --create-ssid-24: create a 2.4GHz SSID")
   print("   scout.py --create-ssid-5: create a 5GHz SSID")
   print("   scout.py --create-ssid-radius-24: create a 2.4GHz RADIUS SSID")
   print("   scout.py --create-ssid-radius-5: create a 5GHz RADIUS SSID")
   print("   scout.py --delete-ssid-24: delete a 2.4GHz SSID")
   print("   scout.py --delete-ssid-5: delete a 5GHz SSID")
   print("   scout.py --delete-ssid-radius-24: delete a 2.4GHz RADIUS SSID")
   print("   scout.py --delete-ssid-radius-5: delete a 5GHz RADIUS SSID")
   print("   scout.py --disable-http: disable access point HTTP server")
   print("   scout.py --disable-radius: disable access point RADIUS function") 
   print("   scout.py --disable-snmp: disable access point SNMP function")
   print("   scout.py --enable-http: enable access point HTTP function")
   print("   scout.py --enable-radius: enable access point RADIUS function")
   print("   scout.py --enable-snmp: enable access point SNMP function")
   print("   scout.py --get-speed: show access point link speed")
   print("   scout.py --tftp-backup: backup access point config via TFTP")
   print("   scout.py --wr: write configuration to access point")
   print("   scout.py --erase: erase configuration on access point")
   print("   scout.py --count-clients: fetch client associations on access point")
   print("   scout.py --get-name: fetch access point hostname via SNMP")
   print("   scout.py --ping: ping access point")
   print("   scout.py --get-mac: fetch access point MAC address via SNMP")
   print("   scout.py --get-model: fetch access point model info via SNMP")
   print("   scout.py --get-serial: fetch access point serial number via SNMP")
   print("   scout.py --get-location: fetch access point location via SNMP")
   print("   scout.py --get-ios-info: fetch access point IOS info via SNMP")
   print("   scout.py --get-uptime: fetch access point uptime info via SNMP")

# cisco_arp.py

if queryCommand == "--get-arp":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                        password = password,
                        look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   arpCommand = remote_conn.recv(65535)
   remote_conn.send("show ip arp\n")
   time.sleep(.10)
   arp = remote_conn.recv(65535)
   print arp

# cisco_led.py

if queryCommand == "--led":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                        password = password,
                        look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("led flash 30\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_change_ap_ip.py

if queryCommand == "--change-ip":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   queryNewIp = sys.argv[5]
   querySubnetMask = sys.argv[6]
   newIp = queryNewIp
   subnetMask = querySubnetMask
   remote_conn_pre=paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port=22, username=username,
                        password=password,
                        look_for_keys=False, allow_agent=False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int BVI1\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('ip address %s %s\n' % (newIp,subnetMask))
   time.sleep(.10)
   output = remote_conn.recv(65535)
# Open Second SSH Connection for New IP (Cardinal)
   remote_conn_pre2=paramiko.SSHClient()
   remote_conn_pre2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre2.connect(newIp, port = 22, username = username,
                        password = password,
                        look_for_keys = False, allow_agent = False)
   remote_conn2 = remote_conn_pre2.invoke_shell()
   output = remote_conn2.recv(65535)
   remote_conn2.send("enable\n")
   time.sleep(.10)
   output = remote_conn2.recv(65535)
   remote_conn2.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn2.recv(65535)
   remote_conn2.send("conf t\n")
   time.sleep(.10)
   output = remote_conn2.recv(65535)
   remote_conn2.send("do wr\n")
   time.sleep(.10)
   output = remote_conn2.recv(65535)

# cisco_configure_ssid.py

if queryCommand == "--create-ssid-24":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   querySSID = sys.argv[5]
   queryWPA2 = sys.argv[6]
   queryVlan = sys.argv[7]
   queryBridgeGroup = sys.argv[8]
   queryRadioSub = sys.argv[9]
   queryGigaSub = sys.argv[10]
   ssid = querySSID
   wpa2pass = queryWPA2
   vlan = queryVlan
   bridgegroup = queryBridgeGroup
   radiosub = queryRadioSub
   gigasub = queryGigaSub
   remote_conn_pre=paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                        password = password,
                        look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("auth open\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid guest-mode\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("auth key-man wpa version 2\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('wpa-psk ascii %s\n' % wpa2pass)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('vlan %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("end\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)  
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d0\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encryption vlan %s mode ciphers aes\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("no shutdown\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d0\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("exit\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int d0.%s\n' % radiosub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int gi0.%s\n' % gigasub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_configure_ssid_5ghz.py

if queryCommand == "--create-ssid-5":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySSID = sys.argv[5]
   queryWPA2 = sys.argv[6]
   queryVlan = sys.argv[7]
   queryBridgeGroup = sys.argv[8]
   queryRadioSub = sys.argv[9]
   queryGigaSub = sys.argv[10]
   ip = queryIP
   username = queryUser
   password = queryPass
   ssid = querySSID
   wpa2pass = queryWPA2
   vlan = queryVlan
   bridgegroup = queryBridgeGroup
   radiosub = queryRadioSub
   gigasub = queryGigaSub
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("auth open\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid guest-mode\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("auth key-man wpa version 2\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('wpa-psk ascii %s\n' % wpa2pass)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('vlan %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("end\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d1\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encryption vlan %s mode ciphers aes\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("no shutdown\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d1\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("exit\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int d1.%s\n' % radiosub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int gi0.%s\n' % gigasub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_configure_ssid_radius.py

if queryCommand == "--create-ssid-radius-24":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySSID = sys.argv[5]
   queryVlan = sys.argv[6]
   queryBridgeGroup = sys.argv[7]
   queryRadioSub = sys.argv[8]
   queryGigaSub = sys.argv[9]
   queryRadiusIP = sys.argv[10]
   querySharedSecret = sys.argv[11]
   queryAuthPort = sys.argv[12]
   queryAcctPort = sys.argv[13]
   queryRadiusTimeout = sys.argv[14]
   queryRadiusGroup = sys.argv[15]
   queryMethodList = sys.argv[16]
   ip = queryIP
   username = queryUser
   password = queryPass
   ssid = querySSID
   vlan = queryVlan
   bridgegroup = queryBridgeGroup
   radiosub = queryRadioSub
   gigasub = queryGigaSub
   radiusip = queryRadiusIP
   sharedsecret = querySharedSecret
   authport = queryAuthPort
   acctport = queryAcctPort
   timeout = queryRadiusTimeout
   radiusgroup = queryRadiusGroup
   methodlist = queryMethodList
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("auth open\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid guest-mode\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('vlan %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("end\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d0\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encryption vlan %s mode ciphers aes\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("no shutdown\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d0\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("exit\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int d0.%s\n' % radiosub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int gi0.%s\n' % gigasub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("aaa new-model\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('radius-server host %s auth-port %s acct-port %s key %s\n' % (radiusip,authport,acctport,sharedsecret))
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('radius-server timeout %s\n' % timeout)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('aaa group server radius %s\n' % radiusgroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('server %s auth-port %s acct-port %s\n' % (radiusip,authport,acctport))
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('aaa authentication login %s group %s\n' % (methodlist,radiusgroup))
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('authentication open eap %s\n' % methodlist)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('authentication network-eap %s\n' % methodlist)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("authentication key-man wpa version 2\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_configure_ssid_radius_5ghz.py

if queryCommand == "--create-ssid-radius-5":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySSID = sys.argv[5]
   queryVlan = sys.argv[6]
   queryBridgeGroup = sys.argv[7]
   queryRadioSub = sys.argv[8]
   queryGigaSub = sys.argv[9]
   queryRadiusIP = sys.argv[10]
   querySharedSecret = sys.argv[11]
   queryAuthPort = sys.argv[12]
   queryAcctPort = sys.argv[13]
   queryRadiusTimeout = sys.argv[14]
   queryRadiusGroup = sys.argv[15]
   queryMethodList = sys.argv[16]
   ip = queryIP
   username = queryUser
   password = queryPass
   ssid = querySSID
   vlan = queryVlan
   bridgegroup = queryBridgeGroup
   radiosub = queryRadioSub
   gigasub = queryGigaSub
   radiusip = queryRadiusIP
   sharedsecret = querySharedSecret
   authport = queryAuthPort
   acctport = queryAcctPort
   timeout = queryRadiusTimeout
   radiusgroup = queryRadiusGroup
   methodlist = queryMethodList
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("auth open\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid guest-mode\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('vlan %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("end\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d1\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("mbssid\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encryption vlan %s mode ciphers aes\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("no shutdown\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d1\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("exit\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int d1.%s\n' % radiosub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('int gi0.%s\n' % gigasub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('encapsulation dot1q %s\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('bridge-group %s\n' % bridgegroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("aaa new-model\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('radius-server host %s auth-port %s acct-port %s key %s\n' % (radiusip,authport,acctport,sharedsecret))
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('radius-server timeout %s\n' % timeout)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('aaa group server radius %s\n' % radiusgroup)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('server %s auth-port %s acct-port %s\n' % (radiusip,authport,acctport))
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('aaa authentication login %s group %s\n' % (methodlist,radiusgroup))
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('authentication open eap %s\n' % methodlist)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('authentication network-eap %s\n' % methodlist)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("authentication key-man wpa version 2\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_delete_ssid.py

if queryCommand == "--delete-ssid-24":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySSID = sys.argv[5]
   queryVlan = sys.argv[6]
   queryRadioSub = sys.argv[7]
   queryGigaSub = sys.argv[8]
   ip = queryIP
   username = queryUser
   password = queryPass
   ssid = querySSID
   vlan = queryVlan
   radiosub = queryRadioSub
   gigasub = queryGigaSub
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no int d0.%s\n' % radiosub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no int gi0.%s\n' % gigasub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d0\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no encryption vlan %s mode ciphers aes-ccm\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_delete_ssid_5ghz.py

if queryCommand == "--delete-ssid-5":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySSID = sys.argv[5]
   queryVlan = sys.argv[6]
   queryRadioSub = sys.argv[7]
   queryGigaSub = sys.argv[8]
   ip = queryIP
   username = queryUser
   password = queryPass
   ssid = querySSID
   vlan = queryVlan
   radiosub = queryRadioSub
   gigasub = queryGigaSub
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no int d1.%s\n' % radiosub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no int gi0.%s\n' % gigasub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d1\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no encryption vlan %s mode ciphers aes-ccm\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_delete_ssid_radius.py

if (queryCommand == "--delete-ssid-radius-24") or (queryCommand == "--delete-ssid-radius-5"):
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySSID = sys.argv[5]
   queryVlan = sys.argv[6]
   queryRadioSub = sys.argv[7]
   queryGigaSub = sys.argv[8]
   ip = queryIP
   username = queryUser
   password = queryPass
   ssid = querySSID
   vlan = queryVlan
   radiosub = queryRadioSub
   gigasub = queryGigaSub
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no dot11 ssid %s\n' % ssid)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no int d0.%s\n' % radiosub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no int gi0.%s\n' % gigasub)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("int d0\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no encryption vlan %s mode ciphers aes-ccm\n' % vlan)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_disable_http.py

if queryCommand == "--disable-http":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,  
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("no ip http server\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_disable_radius.py

if queryCommand == "--disable-radius":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,  
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("no aaa new-model\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_disable_snmp.py

if queryCommand == "--disable-snmp":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySNMP = sys.argv[5]
   ip = queryIP
   username = queryUser
   password = queryPass
   snmp = querySNMP
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no snmp-server community %s RW\n' % snmp)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('no snmp-server system-shutdown\n')
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_enable_http.py

if queryCommand == "--enable-http":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,  
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("ip http server\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_enable_radius.py

if queryCommand == "--enable-radius":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,  
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("aaa new-model\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_enable_snmp.py

if queryCommand == "--enable-snmp":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   querySNMP = sys.argv[5]
   ip = queryIP
   username = queryUser
   password = queryPass
   snmp = querySNMP
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("conf t\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('snmp-server community %s RW\n' % snmp)
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('snmp-server system-shutdown\n')
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("do wr\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_get_speed.py

if queryCommand == "--get-speed":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("sho int gi0\n")
   time.sleep(.10)
   sshBandwidth = remote_conn.recv(65535)
   getBandwidth = subprocess.check_output("echo '%s' | grep -E -o '.{4}Mbps' | tr -d 'Mbps'"%sshBandwidth, shell=True)
   bandwidthSqlCursor = conn.cursor()
   bandwidthSql = "UPDATE access_points SET ap_bandwidth = '%s' WHERE ap_ip = '%s'" % (getBandwidth,ip)
   bandwidthSqlCursor.execute(bandwidthSql)
   conn.commit()

# cisco_tftp_backup.py

if queryCommand == "--tftp-backup":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   queryTFTP = sys.argv[5]
   queryTFTPName = sys.argv[6]
   ip = queryIP
   username = queryUser
   password = queryPass
   tftp = queryTFTP
   tftpname = queryTFTPName
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("copy running-config tftp\n")
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % tftp)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % tftpname)
   time.sleep(.15)
   output = remote_conn.recv(65535)

# cisco_wr.py

if queryCommand == "--wr":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("wr\n")
   time.sleep(.15)
   output = remote_conn.recv(65535)

# cisco_write_default.py

if queryCommand == "--erase":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   output = remote_conn.recv(65535)
   remote_conn.send("enable\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send('%s\n' % password)
   time.sleep(.15)
   output = remote_conn.recv(65535)
   remote_conn.send("write default\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("y\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("reload\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)
   remote_conn.send("y\n")
   time.sleep(.10)
   output = remote_conn.recv(65535)

# cisco_count_clients.py

if queryCommand == "--count-clients":
   queryIP = sys.argv[2]
   queryUser = sys.argv[3]
   queryPass = sys.argv[4]
   ip = queryIP
   username = queryUser
   password = queryPass
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(ip, port = 22, username = username,
                           password = password,
                           look_for_keys = False, allow_agent = False)
   remote_conn = remote_conn_pre.invoke_shell()
   countCommand = remote_conn.recv(65535)
   remote_conn.send("show dot11 associations\n")
   time.sleep(.10)
   countClient = remote_conn.recv(65535)
   getClient = subprocess.check_output("echo '%s' | grep -o [0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f] | wc -l"%countClient, shell=True)
   clientSqlCursor = conn.cursor()
   clientSql = "UPDATE access_points SET ap_total_clients = '%s' WHERE ap_ip = '%s'" % (getClient,ip)
   clientSqlCursor.execute(clientSql)
   conn.commit()

# --get-name

if queryCommand == "--get-name":
   queryIP = sys.argv[2]
   querySNMP = sys.argv[3]
   ip = queryIP
   snmp = querySNMP
   getApName = subprocess.check_output("snmpget -Oqv -v2c -c '%s' '%s' iso.3.6.1.2.1.1.5.0" % (snmp,ip), shell=True)
   sqlApName = getApName.replace('"', '')
   apNameCursor = conn.cursor()
   apNameSql = "UPDATE access_points SET ap_name = '%s' WHERE ap_ip = '%s'" % (sqlApName,ip)
   apNameCursor.execute(apNameSql)
   conn.commit() 

# --get-mac

if queryCommand == "--get-mac":
   queryIP = sys.argv[2]
   querySNMP = sys.argv[3]
   ip = queryIP
   snmp = querySNMP
   getApMac = subprocess.check_output("snmpget -Oqv -v2c -c '%s' '%s' iso.3.6.1.2.1.2.2.1.6.3" % (snmp,ip), shell=True)
   sqlApMac = getApMac.replace('"', '')
   apMacCursor = conn.cursor()
   apMacSql = "UPDATE access_points SET ap_mac_addr = '%s' WHERE ap_ip = '%s'" % (sqlApMac,ip)
   apMacCursor.execute(apMacSql)
   conn.commit()

# --ping

if queryCommand == "--ping":
   queryIP = sys.argv[2]
   ip = queryIP
   pingAp = subprocess.check_output("ping '%s' -c 10| head -n 2 | tail -n 1 | awk '{print $7}' | tr -d 'time='"%ip, shell=True)
   pingApCursor = conn.cursor()
   pingApSql = "UPDATE access_points SET ap_ping_ms = '%s' WHERE ap_ip = '%s'" % (pingAp,ip)
   pingApCursor.execute(pingApSql)
   conn.commit()

# --get-model

if queryCommand == "--get-model":
   queryIP = sys.argv[2]
   querySNMP = sys.argv[3]
   ip = queryIP
   snmp = querySNMP
   getApModel = subprocess.check_output("snmpget -Oqv -v2c -c '%s' '%s' iso.3.6.1.2.1.47.1.1.1.1.13.1" % (snmp,ip), shell=True)
   sqlApModel = getApModel.replace('"', '')
   apModelCursor = conn.cursor()
   apModelSql = "UPDATE access_points SET ap_model = '%s' WHERE ap_ip = '%s'" % (sqlApModel,ip)
   apModelCursor.execute(apModelSql)
   conn.commit()

# --get-serial

if queryCommand == "--get-serial":
   queryIP = sys.argv[2]
   querySNMP = sys.argv[3]
   ip = queryIP
   snmp = querySNMP
   getApSerial = subprocess.check_output("snmpget -Oqv -v2c -c '%s' '%s' iso.3.6.1.2.1.47.1.1.1.1.11.1" % (snmp,ip), shell=True)
   sqlApSerial = getApSerial.replace('"', '')
   apSerialCursor = conn.cursor()
   apSerialSql = "UPDATE access_points SET ap_serial = '%s' WHERE ap_ip = '%s'" % (sqlApSerial,ip)
   apSerialCursor.execute(apSerialSql)
   conn.commit()

# --get-location

if queryCommand == "--get-location":
   queryIP = sys.argv[2]
   querySNMP = sys.argv[3]
   ip = queryIP
   snmp = querySNMP
   getApLocation = subprocess.check_output("snmpget -Oqv -v2c -c '%s' '%s' iso.3.6.1.2.1.1.6.0" % (snmp,ip), shell=True)
   sqlApLocation = getApLocation.replace('"', '')
   apLocationCursor = conn.cursor()
   apLocationSql = "UPDATE access_points SET ap_location = '%s' WHERE ap_ip = '%s'" % (sqlApLocation,ip)
   apLocationCursor.execute(apLocationSql)
   conn.commit()

# --get-ios-info

if queryCommand == "--get-ios-info":
   queryIP = sys.argv[2]
   querySNMP = sys.argv[3]
   ip = queryIP
   snmp = querySNMP
   getApIos = subprocess.check_output("snmpget -Oqv -v2c -c '%s' '%s' iso.3.6.1.2.1.1.1.0" % (snmp,ip), shell=True)
   sqlApIos = getApIos.replace('"', '')
   apIosCursor = conn.cursor()
   apIosSql = "UPDATE access_points SET ap_ios_info = '%s' WHERE ap_ip = '%s'" % (sqlApIos,ip)
   apIosCursor.execute(apIosSql)
   conn.commit()

# --get-uptime

if queryCommand == "--get-uptime":
   queryIP = sys.argv[2]
   querySNMP = sys.argv[3]
   ip = queryIP
   snmp = querySNMP
   getApUptime = subprocess.check_output("snmpget -Oqv -v2c -c '%s' '%s' iso.3.6.1.2.1.1.3.0" % (snmp,ip), shell=True)
   sqlApUptime = getApUptime.replace('"', '')
   apUptimeCursor = conn.cursor()
   apUptimeSql = "UPDATE access_points SET ap_uptime = '%s' WHERE ap_ip = '%s'" % (sqlApUptime,ip)
   apUptimeCursor.execute(apUptimeSql)
   conn.commit()

