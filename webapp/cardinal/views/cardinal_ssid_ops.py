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

from cardinal.system.cardinal_sys import cardinalSql
from cardinal.system.cardinal_sys import MySQLdb
from cardinal.system.cardinal_sys import cipherSuite
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from scout import scout_ssid

cardinal_ssid_ops = Blueprint('cardinal_ssid_ops_bp', __name__)

@cardinal_ssid_ops.route("/do-deploy-ssid-24ghz", methods=["POST"])
def doDeploySsid24Ghz():
    conn = cardinalSql()
    ssidId = request.form["ssid_id"]
    apId = session.get('apId')
    apName = session.get('apName')
    try:
        checkSsidRelationship = conn.cursor()
        checkSsidRelationship.execute("INSERT INTO ssids_24ghz_deployed (ap_id,ssid_id) VALUES ('{}', '{}')".format(apId,ssidId))
        checkSsidRelationship.close()
    except MySQLdb.Error as e:
        status = "MySQL Error: {}".format(e)
        return redirect(url_for('cardinal_ssid_bp.deploySsid24Ghz', status=status))
    except MySQLdb.IntegrityError as e:
        status = "IntegrityError: {0} ran into a conflict: {1}".format(apName,e)
        return redirect(url_for('cardinal_ssid_bp.deploySsid24Ghz', status=status))
    else:
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        ssidInfoCursor = conn.cursor()
        ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = '{}'".format(ssidId))
        ssidInfo = ssidInfoCursor.fetchall()
        for ssidData in ssidInfo:
            ssid = ssidData[0]
            vlan = ssidData[1]
            wpa2Pass = ssidData[2]
            bridgeGroup = ssidData[3]
            radioSub = ssidData[4]
            gigaSub = ssidData[5]
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_ssid.scoutCreateSsid24(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssid, vlan=vlan, wpa2Pass=wpa2Pass, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub)
        status = "Deployment of 2.4GHz SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssid,apName)
    finally:
        conn.commit()
        conn.close()
        return redirect(url_for('cardinal_ssid_bp.deploySsid24Ghz', status=status))

@cardinal_ssid_ops.route("/do-deploy-ssid-24ghz-group", methods=["POST"])
def doDeploySsid24GhzGroup():
    conn = cardinalSql()
    ssidId = request.form["ssid_id"]
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    apGroupCheck = conn.cursor()
    apGroupCheck.execute("SELECT ap_id FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
    apIdsSql = apGroupCheck.fetchall()
    apGroupCheck.close()
    apIds = []
    for value in apIdsSql:
        apIds.append(value[0])
    for apId in apIds:
        try:
            checkSsidRelationship = conn.cursor()
            checkSsidRelationship.execute("INSERT INTO ssids_24ghz_deployed (ap_id,ssid_id) VALUES ('{}', '{}')".format(apId,ssidId))
            checkSsidRelationship.close()
        except MySQLdb.Error as e:
            getApName = conn.cursor()
            getApName.execute("SELECT ap_name FROM access_points WHERE ap_id = '{}'".format(apId))
            apName = getApName.fetchone()[0]
            getApName.close()
            conn.close()
            status = "MySQL Error: {0} ran into an error: {1}".format(apName,e)
            return redirect(url_for('cardinal_ssid_bp.deploySsid24GhzGroup', status=status))
        else:
            apInfoCursor = conn.cursor()
            apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
            apInfo = apInfoCursor.fetchall()
            apInfoCursor.close()
            ssidInfoCursor = conn.cursor()
            ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = '{}'".format(ssidId))
            ssidInfo = ssidInfoCursor.fetchall()
            ssidInfoCursor.close()
            for ssidData in ssidInfo:
                ssid = ssidData[0]
                vlan = ssidData[1]
                wpa2Pass = ssidData[2]
                bridgeGroup = ssidData[3]
                radioSub = ssidData[4]
                gigaSub = ssidData[5]
            for info in apInfo:
                apIp = info[0]
                apSshUsername = info[1]
                encryptedSshPassword = bytes(info[3], 'utf-8')
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
            scout_ssid.scoutCreateSsid24(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssid, vlan=vlan, wpa2Pass=wpa2Pass, bridgeGroup=bridgeGroup, radioSub=radioSub, gigaSub=gigaSub)
            status = "Deployment of 2.4GHz SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssid,apGroupName)
            conn.commit()
    conn.close()
    return redirect(url_for('cardinal_ssid_bp.deploySsid24GhzGroup', status=status))

@cardinal_ssid_ops.route("/do-remove-ssid-24ghz", methods=["POST"])
def doRemoveSsid24Ghz():
    conn = cardinalSql()
    ssidId = request.form["ssid_id"]
    apId = session.get('apId')
    apName = session.get('apName')
    try:
        checkSsidRelationship = conn.cursor()
        checkSsidRelationship.execute("DELETE FROM ssids_24ghz_deployed WHERE ap_id = {0} AND ssid_id = {1}".format(apId,ssidId))
        checkSsidRelationship.close()
    except MySQLdb.Error as e:
        status = "MySQL Error: {0} ran into a conflict: {1}".format(apName,e)
        return redirect(url_for('cardinal_ssid_bp.removeSsid24Ghz', status=status))
    else:
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        ssidInfoCursor = conn.cursor()
        ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = '{}'".format(ssidId))
        ssidInfo = ssidInfoCursor.fetchall()
        for ssidData in ssidInfo:
            ssid = ssidData[0]
            vlan = ssidData[1]
            radioSub = ssidData[2]
            gigaSub = ssidData[3]
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_ssid.scoutDeleteSsid24(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
        status = "Removal of 2.4GHz SSID {0} from AP {1} Has Been Successfully Initiated!".format(ssid,apName)
    finally:
        conn.commit()
        conn.close()
        return redirect(url_for('cardinal_ssid_bp.removeSsid24Ghz', status=status))
