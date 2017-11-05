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
queryBridgeGroup = sys.argv[6]
queryRadioSub = sys.argv[7]
queryGigaSub = sys.argv[8]
queryRadiusIP = sys.argv[9]
querySharedSecret = sys.argv[10]
queryAuthPort = sys.argv[11]
queryAcctPort = sys.argv[12]
queryRadiusTimeout = sys.argv[13]
queryRadiusGroup = sys.argv[14]
queryMethodList = sys.argv[15]

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

remote_conn.send('dot11 ssid %s\n' % ssid)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("auth open\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("mbssid guest-mode\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('vlan %s\n' % vlan)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("end\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("conf t\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("int d0\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("mbssid\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('encryption vlan %s mode ciphers aes\n' % vlan)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("no shutdown\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('dot11 ssid %s\n' % ssid)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("int d0\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('ssid %s\n' % ssid)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("exit\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('int d0.%s\n' % radiosub)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('encapsulation dot1q %s\n' % vlan)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('bridge-group %s\n' % bridgegroup)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('int gi0.%s\n' % gigasub)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('encapsulation dot1q %s\n' % vlan)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('bridge-group %s\n' % bridgegroup)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("aaa new-model\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('radius-server host %s auth-port %s acct-port %s key %s\n' % (radiusip,authport,acctport,sharedsecret))
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('radius-server timeout %s\n' % timeout)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('aaa group server radius %s\n' % radiusgroup)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('server %s auth-port %s acct-port %s\n' % (radiusip,authport,acctport))
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('aaa authentication login %s group %s\n' % (methodlist,radiusgroup))
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('dot11 ssid %s\n' % ssid)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('authentication open eap %s\n' % methodlist)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send('authentication network-eap %s\n' % methodlist)
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("authentication key-man wpa version 2\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("do wr\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

exit()
