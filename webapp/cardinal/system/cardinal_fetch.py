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

import os
import schedule
import scout_info
import time
from configparser import ConfigParser
from cardinal_sys import cardinalSql
from cardinal_sys import cipherSuite
from cardinal_sys import MySQLdb

# FETCHER CONFIG

cardinalConfigFile = os.environ['CARDINALCONFIG']
cardinalConfig = ConfigParser()
cardinalConfig.read("{}".format(cardinalConfigFile))
fetcherInterval = cardinalConfig.get('cardinal', 'fetchinterval')

def fetcher():
    """Uses the scout_info library to fetch access point information and populate the DB."""
    print("INFO: Running command calls via scout_info...")
    startTime = time.time()
    conn = cardinalSql()
    apIdCursor = conn.cursor()
    apIdCursor.execute("SELECT ap_id FROM access_points WHERE ap_all_id = '2'")
    apIdsSql = apIdCursor.fetchall()
    apIdCursor.close()
    apIds = []
    for value in apIdsSql:
        apIds.append(value[0])
    for apId in apIds:
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apIp = info[0]
            apSshUsername = info[1]
            encryptedSshPassword = bytes(info[2], 'utf-8')
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        # Use a try..except to fetch access point information
        try:
            apBandwidth = scout_info.scoutGetSpeed(ip=apIp, username=apSshUsername, password=apSshPassword)
            apMacAddr = scout_info.scoutGetMac(ip=apIp, username=apSshUsername, password=apSshPassword)
            apModel = scout_info.scoutGetModel(ip=apIp, username=apSshUsername, password=apSshPassword)
            apSerial = scout_info.scoutGetSerial(ip=apIp, username=apSshUsername, password=apSshPassword)
            apLocation = scout_info.scoutGetLocation(ip=apIp, username=apSshUsername, password=apSshPassword)
            apIosInfo = scout_info.scoutGetIosInfo(ip=apIp, username=apSshUsername, password=apSshPassword)
            apUptime = scout_info.scoutGetUptime(ip=apIp, username=apSshUsername, password=apSshPassword)
            inputSqlCursor = conn.cursor()
            inputSqlCursor.execute("UPDATE access_points SET ap_bandwidth = '{0}' WHERE ap_id = '{1}'".format(apBandwidth,apId))
            inputSqlCursor.execute("UPDATE access_points SET ap_mac_addr = '{0}' WHERE ap_id = '{1}'".format(apMacAddr,apId))
            inputSqlCursor.execute("UPDATE access_points SET ap_model = '{0}' WHERE ap_id = '{1}'".format(apModel,apId))
            inputSqlCursor.execute("UPDATE access_points SET ap_serial = '{0}' WHERE ap_id = '{1}'".format(apSerial,apId))
            inputSqlCursor.execute("UPDATE access_points SET ap_location = '{0}' WHERE ap_id = '{1}'".format(apLocation,apId))
            inputSqlCursor.execute("UPDATE access_points SET ap_ios_info = '{0}' WHERE ap_id = '{1}'".format(apIosInfo,apId))
            inputSqlCursor.execute("UPDATE access_points SET ap_uptime = '{0}' WHERE ap_id = '{1}'".format(apUptime,apId))
            inputSqlCursor.close()
            conn.commit()
        except MySQLdb.Error as e:
            print("ERROR: {}".format(e))
    completionTime = "INFO: cardinal_fetch completed in:", time.time() - startTime
    conn.close()
    return completionTime

# RUN fetch() ON INTERVAL

schedule.every(int('{}'.format(fetcherInterval))).minutes.do(fetcher)

while True:
    schedule.run_pending()
