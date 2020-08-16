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

# THIS IS ONLY A TEST FILE

import MySQLdb
from configparser import ConfigParser

# MySQL authentication

mysqlConfig = ConfigParser()
mysqlConfig.read("ci/cardinal.ini")
mysqlHost = mysqlConfig.get('cardinal', 'dbserver')
mysqlUser = mysqlConfig.get('cardinal', 'dbuser')
mysqlPass = mysqlConfig.get('cardinal', 'dbpassword')
mysqlDb = mysqlConfig.get('cardinal', 'dbname')

def cardinalSql():
    conn = MySQLdb.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPass, db = mysqlDb)
    return conn

try:
    conn = cardinalSql()
    testCursor = conn.cursor()
    testCursor.execute("SELECT VERSION()")
    version = testCursor.fetchone()[0]
    if version:
        print("CONNECTION TEST PASSED: {}".format(version))
    else:
        print("CONNECTION TEST FAILED: {}".format(MySQLdb.Error))
    conn.close()
except MySQLdb.Error as e:
    conn.close()
    print("Cardinal detected a MySQL error: {}".format(e))
