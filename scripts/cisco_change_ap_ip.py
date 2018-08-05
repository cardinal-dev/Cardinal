#!/usr/bin/python

import paramiko
import time
import sys

queryIP = sys.argv[1]
queryUser = sys.argv[2]
queryPass = sys.argv[3]
queryNewIP = sys.argv[4]
querySubnetMask = sys.argv[5]

ip = queryIP
username = queryUser
password = queryPass
newip = queryNewIP
subnetmask = querySubnetMask

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

remote_conn.send('ip address %s %s\n' % (newip,subnetmask))
time.sleep(.10)
output = remote_conn.recv(65535)

# Open Second SSH Connection for New IP (Cardinal)

remote_conn_pre2=paramiko.SSHClient()
remote_conn_pre2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre2.connect(newip, port=22, username=username,
                        password=password,
                        look_for_keys=False, allow_agent=False)

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

exit()

