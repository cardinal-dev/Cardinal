#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2019 Cardinal Contributors

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

import logging
import MySQLdb
import os
from configparser import ConfigParser
from cryptography.fernet import Fernet

# SYSTEM VARIABLES

cardinalConfigFile = os.environ['CARDINALCONFIG']
cardinalConfig = ConfigParser()
devourSettings = cardinalConfig.read("{}".format(cardinalConfigFile))
cardinalLogFile = cardinalConfig.get('cardinal', 'logfile')
logging.basicConfig(filename='{}'.format(cardinalLogFile), filemode='w', format='%(name)s - %(levelname)s - %(message)s')
flaskKey = cardinalConfig.get('cardinal', 'flaskkey')
encryptKey = cardinalConfig.get('cardinal', 'encryptkey')
bytesKey = bytes(encryptKey, 'utf-8')
cipherSuite = Fernet(bytesKey)

# MySQL AUTHENTICATION & HANDLING

mysqlHost = cardinalConfig.get('cardinal', 'dbserver')
mysqlUser = cardinalConfig.get('cardinal', 'dbuser')
mysqlPass = cardinalConfig.get('cardinal', 'dbpassword')
mysqlDb = cardinalConfig.get('cardinal', 'dbname')

def cardinalSql():
    conn = MySQLdb.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPass, db = mysqlDb)
    return conn
