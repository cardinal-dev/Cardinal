#!/usr/bin/python

import paramiko
from getpass import getpass
import time
import sys

queryIP = sys.argv[1]
queryUser = sys.argv[2]
queryPass = sys.argv[3]
querySSID = sys.argv[4]
queryVlan = sys.argv[5]
queryRadioSub = sys.argv[6]
queryGigaSub = sys.argv[7]

ip = queryIP
username = queryUser
password = queryPass
ssid = querySSID
vlan = queryVlan
radiosub = queryRadioSub
gigasub = queryGigaSub

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip, port=22, username=username,
                        password=password,
                        look_for_keys=False, allow_agent=False)

remote_conn = remote_conn_pre.invoke_shell()
output = remote_conn.recv(65535)
print output

remote_conn.send("enable\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('%s\n' % password)
time.sleep(.15)
output = remote_conn.recv(65535)
print output

remote_conn.send("conf t\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('no dot11 ssid %s\n' % ssid)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('no int d1.%s\n' % radiosub)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('no int gi0.%s\n' % gigasub)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("int d1\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('no encryption vlan %s mode ciphers aes-ccm\n' % vlan)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("do wr\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

exit()

