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

remote_conn.send("show ip arp\n")
time.sleep(.10)
output = remote_conn.recv(65535)

exit()
