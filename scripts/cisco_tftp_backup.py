#!/usr/bin/python

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

queryIP = sys.argv[1]
queryUser = sys.argv[2]
queryPass = sys.argv[3]
queryTFTP = sys.argv[4]
queryTFTPName = sys.argv[5]

ip = queryIP
username = queryUser
password = queryPass
tftp = queryTFTP
tftpname = queryTFTPName

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


remote_conn.send("copy running-config tftp\n")
time.sleep(.15)
output = remote_conn.recv(65535)


remote_conn.send('%s\n' % tftp)
time.sleep(.15)
output = remote_conn.recv(65535)


remote_conn.send('%s\n' % tftpname)
time.sleep(.15)
output = remote_conn.recv(65535)


exit()

