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

import MySQLdb
import scout_info
import time
from configparser import ConfigParser
from cardinal.system.cardinal_sys import cardinalSql
from cardinal.system.cardinal_sys import cipherSuite
from datetime import datetime

timeStamp = datetime.now()

def gatherApInfo(apId):
    """Uses scoutFetcher() to fetch access point information and populate the DB."""
    startTime = time.time()
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
    apInfo = apInfoCursor.fetchall()
    apInfoCursor.close()
    for info in apInfo:
        apName = info[0]
        apIp = info[1]
        apSshUsername = info[2]
        encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
    # Use a try..except to fetch access point information
    try:
        apInfo = scout_info.scoutFetcher(ip=apIp, username=apSshUsername, password=apSshPassword)
        apMacAddr = apInfo[0]
        apBandwidth = apInfo[1].strip("Mbps")
        apIosInfo = apInfo[2]
        apUptime = apInfo[3]
        apSerial = apInfo[4]
        apModel = apInfo[5]
        apClientCount = apInfo[6]
        apLocation = apInfo[7]
        inputSqlCursor = conn.cursor()
        inputSqlCursor.execute("UPDATE access_points SET ap_bandwidth = %s, ap_mac_addr = %s, ap_model = %s, ap_serial = %s, ap_location = %s,"
        "ap_ios_info = %s, ap_uptime = %s, ap_total_clients = %s WHERE ap_id = %s", (apBandwidth,apMacAddr,apModel,apSerial,
        apLocation,apIosInfo,apUptime,apClientCount,apId))
        inputSqlCursor.close()
        conn.commit()
    except MySQLdb.Error as e:
        return "{0} ERROR: {1}".format(timeStamp,e)
    endTime = time.time()
    completionTime = endTime - startTime
    status = "{0} INFO: Gathered access point information for {1} in: {2}".format(timeStamp,apName,completionTime)
    conn.close()
    return status

def gatherAllApInfo():
    """Uses scoutFetcher() to fetch access point information and populate the DB (for all APs)"""
    conn = cardinalSql()
    apIdCursor = conn.cursor()
    apIdCursor.execute("SELECT ap_id FROM access_points WHERE ap_all_id = 2")
    apIdsSql = apIdCursor.fetchall()
    apIdCursor.close()
    for apId in apIdsSql:
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password,ap_name FROM access_points WHERE ap_id = %s", [apId])
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apIp = info[0]
            apSshUsername = info[1]
            encryptedSshPassword = bytes(info[2], 'utf-8')
            apName = info[3]
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        # Use a try..except to fetch access point information
        try:
            startTime = time.time()
            apInfo = scout_info.scoutFetcher(ip=apIp, username=apSshUsername, password=apSshPassword)
            apMacAddr = apInfo[0]
            apBandwidth = apInfo[1].strip("Mbps")
            apIosInfo = apInfo[2]
            apUptime = apInfo[3]
            apSerial = apInfo[4]
            apModel = apInfo[5]
            apClientCount = apInfo[6]
            apLocation = apInfo[7]
            inputSqlCursor = conn.cursor()
            inputSqlCursor.execute("UPDATE access_points SET ap_bandwidth = %s, ap_mac_addr = %s, ap_model = %s, ap_serial = %s, ap_location = %s,"
            "ap_ios_info = %s, ap_uptime = %s, ap_total_clients = %s WHERE ap_id = %s", (apBandwidth,apMacAddr,apModel,apSerial,
            apLocation,apIosInfo,apUptime,apClientCount,apId))
            inputSqlCursor.close()
            conn.commit()
            endTime = time.time()
            completionTime = endTime - startTime
            status = "{0} INFO: Gathered device information for {1} in: {2}".format(timeStamp,apName,completionTime)
            print(status)
        except MySQLdb.Error as e:
            return ("{0} ERROR: {1}".format(timeStamp,e))
        return status
    conn.close()
