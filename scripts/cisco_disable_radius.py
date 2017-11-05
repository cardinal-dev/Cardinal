#!/usr/bin/python

import paramiko
from getpass import getpass
import time
import sys

queryIP = sys.argv[1]
queryUser = sys.argv[2]
queryPass = sys.argv[3]

ip = queryIP
username = queryUser
password = queryPass

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

remote_conn.send("no aaa new-model\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

remote_conn.send("do wr\n")
time.sleep(.10)
output = remote_conn.recv(65535)
print output

exit()
