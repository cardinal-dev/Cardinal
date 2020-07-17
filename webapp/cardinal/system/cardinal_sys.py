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
import multiprocessing
import os
from configparser import ConfigParser
from cryptography.fernet import Fernet

cardinalConfigFile = os.environ['CARDINALCONFIG']
cardinalConfig = ConfigParser()
cardinalConfig.read("{}".format(cardinalConfigFile))

# SYSTEM VARIABLES

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
    """Connection object for MySQLdb transactions."""
    conn = MySQLdb.connect(host=mysqlHost, user=mysqlUser, passwd=mysqlPass, db=mysqlDb)
    return conn

# GROUP OPERATIONS

def printCompletionTime(endTime):
    """Just prints completion time for parallel group processes."""
    completionTime = "INFO: Group Operation Completed In: {}".format(endTime)
    return completionTime

def apGroupIterator(apGroupId, snmp="False", **kwargs):
    """apGroupIterator() is used to create a list of lists, which is then passed
    into functions such as processor()."""
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    if snmp == "True":
        apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password,ap_snmp FROM access_points WHERE ap_group_id = %s", [apGroupId])
    elif snmp == "False":
        apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = %s", [apGroupId])
    apInfoSql = apInfoCursor.fetchall()
    apInfoCursor.close()
    apList = []
    for info in apInfoSql:
        connInfo = []
        apIp = connInfo.append(info[0])
        apSshUsername = connInfo.append(info[1])
        encryptedSshPassword = bytes(info[2], 'utf-8')
        apSshPassword = connInfo.append(cipherSuite.decrypt(encryptedSshPassword).decode('utf-8'))
        if snmp == "True":
            encryptedSnmp = bytes(info[3], 'utf-8')
            apSnmp = connInfo.append(cipherSuite.decrypt(encryptedSnmp).decode('utf-8'))
        addedArgs = list(kwargs.values())
        apInfo = connInfo + addedArgs # Combine the two lists into one named apInfo[].
        apList.append(apInfo)
    conn.close()
    return apList

# GROUP PROCESSING

def processor(operation, apInfo):
    """processor() is used for parallel processing. processor()
    accepts two positional arguments: operation and apInfo. operation is
    the function itself (e.g. scout_sys.scoutDoWr) and apInfo is a list of parameters
    that is passed for each access point (e.g. connection information)."""
    workers = cardinalConfig.get('cardinal', 'workers')
    with multiprocessing.Pool(processes=int(workers)) as tasker:
        taskResults = tasker.starmap(operation, apInfo)
    return taskResults

# SSID DEPLOYMENT

def ssidCheck(apId, ssidId, ssidType=None, action=None):
    """Accepts four positional arguments: apId and ssidId.
    ssidCheck() is used to determine whether or not an access point
    has a specific SSID associated. True means that ssidCheck is successful
    and the AP does not have the SSID deployed. False means ssidCheck
    was not successful and the AP already has the SSID deployed. ssidType
    supports four arguments: ssid_24ghz, ssid_24ghz_radius, ssid_5ghz,
    ssid_5ghz_radius. action support two arguments: commit and test. commit will
    actually commit the new deployment to the database, while test just sees if
    the result would pass, without committing (i.e. dry-run)."""
    conn = cardinalSql()
    try:
        checkSsidRelationship = conn.cursor()
        if ssidType == "ssid_24ghz":
            checkSsidRelationship.execute("INSERT INTO ssids_24ghz_deployed (ap_id,ssid_id) VALUES (%s, %s)", (apId,ssidId))
        elif ssidType == "ssid_24ghz_radius":
            checkSsidRelationship.execute("INSERT INTO ssids_24ghz_radius_deployed (ap_id,ssid_id) VALUES (%s, %s)", (apId,ssidId))
        elif ssidType == "ssid_5ghz":
            checkSsidRelationship.execute("INSERT INTO ssids_5ghz_deployed (ap_id,ssid_id) VALUES (%s, %s)", (apId,ssidId))
        elif ssidType == "ssid_5ghz_radius":
            checkSsidRelationship.execute("INSERT INTO ssids_5ghz_radius_deployed (ap_id,ssid_id) VALUES (%s, %s)", (apId,ssidId))
        else:
            return None
        checkSsidRelationship.close()
    except MySQLdb.Error:
        conn.close()
        return False
    else:
        if action == "test":
            conn.close()
            return True
        elif action == "commit":
            conn.commit()
            conn.close()
            return True
        else:
            return None


def ssidGatherApIds(apGroupId):
    """Pulls apIds from MySQL depending on group membership."""
    conn = cardinalSql()
    try:
        apGroupCheck = conn.cursor()
        apGroupCheck.execute("SELECT ap_id FROM access_points WHERE ap_group_id = %s", [apGroupId])
        apIdsSql = apGroupCheck.fetchall()
        apGroupCheck.close()
    except MySQLdb.Error as e:
        conn.close()
        return e
    else:
        conn.close()
        return apIdsSql

def getSsidInfo(ssidId, ssidType=None):
    """Gathers tuple of SSID information based on ssidId,
    which can then be used for SSID deployment operations.
    ssidType options include: ssid_24ghz, ssid_5ghz, ssid_24ghz_radius,
    ssid_5ghz_radius."""
    conn = cardinalSql()
    try:
        ssidInfoCursor = conn.cursor()
        if ssidType == "ssid_24ghz":
            ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = %s", [ssidId])
        elif ssidType == "ssid_24ghz_radius":
            ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [ssidId])
        elif ssidType == "ssid_5ghz":
            ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz WHERE ap_ssid_id = %s", [ssidId])
        elif ssidType == "ssid_5ghz_radius":
            ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [ssidId])
        else:
            return "Invalid ssidType"
        ssidInfo = ssidInfoCursor.fetchall()
        ssidInfoCursor.close()
    except MySQLdb.Error as e:
        conn.close()
        return e
    else:
        conn.close()
        return ssidInfo

# SYSTEM MESSAGES

def msgResourceDeleted(resource):
    msg = "{} was deleted successfully!".format(resource)
    return msg

def msgResourceAdded(resource):
    msg = "{} was registered successfully!".format(resource)
    return msg

def msgSpecifyValidApGroup():
    msg = "Please select a valid access point group."
    return msg

def msgSpecifyValidAp():
    msg = "Please select a valid access point."
    return msg
