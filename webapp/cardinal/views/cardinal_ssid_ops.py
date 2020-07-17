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
import time
from cardinal.system.cardinal_sys import apGroupIterator
from cardinal.system.cardinal_sys import printCompletionTime
from cardinal.system.cardinal_sys import cardinalSql
from cardinal.system.cardinal_sys import cipherSuite
from cardinal.system.cardinal_sys import getSsidInfo
from cardinal.system.cardinal_sys import ssidCheck
from cardinal.system.cardinal_sys import ssidGatherApIds
from cardinal.system.cardinal_sys import processor
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from scout import scout_ssid

cardinal_ssid_ops = Blueprint('cardinal_ssid_ops_bp', __name__)

@cardinal_ssid_ops.route("/deploy-ssid-24ghz", methods=["GET", "POST"])
def deploySsid24Ghz():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-24ghz.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('cardinal_auth_bp.index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_24ghz")
            encryptedWpa2Pass = bytes(ssidInfo[0][2], 'utf-8')
            wpa2Pass = cipherSuite.decrypt(encryptedWpa2Pass).decode('utf-8')
            checkSsidRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_24ghz", action="test")
            if checkSsidRelationship:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                for info in apInfo:
                    apIp = info[0]
                    apSshUsername = info[1]
                    encryptedSshPassword = bytes(info[2], 'utf-8')
                    apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
                scout_ssid.scoutCreateSsid24(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssidInfo[0][0], vlan=ssidInfo[0][1], wpa2Pass=wpa2Pass, bridgeGroup=ssidInfo[0][3], radioSub=ssidInfo[0][4], gigaSub=ssidInfo[0][5])
                commitRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_24ghz", action="commit")
                status = "Deployment of 2.4GHz SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apName)
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid24Ghz', status=status))
            else:
                conn.close()
                status = "2.4GHz SSID {0} is already deployed on {1}".format(ssidInfo[0][0], apName)
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid24Ghz', status=status))

@cardinal_ssid_ops.route("/deploy-ssid-24ghz-radius", methods=["GET", "POST"])
def deploySsid24GhzRadius():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz_radius")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-24ghz-radius.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_24ghz_radius")
            encryptedSharedSecret = bytes(ssidInfo[0][6], 'utf-8')
            sharedSecret = cipherSuite.decrypt(encryptedSharedSecret).decode('utf-8')
            checkSsidRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_24ghz_radius", action="test")
            if checkSsidRelationship:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                for info in apInfo:
                    apIp = info[0]
                    apSshUsername = info[1]
                    encryptedSshPassword = bytes(info[2], 'utf-8')
                    apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
                scout_ssid.scoutCreateSsid24Radius(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssidInfo[0][0], vlan=ssidInfo[0][1], bridgeGroup=ssidInfo[0][2], radioSub=ssidInfo[0][3], gigaSub=ssidInfo[0][4], radiusIp=ssidInfo[0][5], sharedSecret=sharedSecret, authPort=ssidInfo[0][7], acctPort=ssidInfo[0][8], radiusTimeout=ssidInfo[0][9], radiusGroup=ssidInfo[0][10], methodList=ssidInfo[0][11])
                commitRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_24ghz_radius", action="commit")
                status = "Deployment of 2.4GHz RADIUS SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apName)
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid24GhzRadius', status=status))
            else:
                conn.close()
                status = "2.4GHz RADIUS SSID {0} is already deployed on {1}".format(ssidInfo[0][0], apName)
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid24GhzRadius', status=status))

@cardinal_ssid_ops.route("/deploy-ssid-24ghz-group", methods=["GET", "POST"])
def deploySsid24GhzGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-24ghz-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_24ghz")
            encryptedWpa2Pass = bytes(ssidInfo[0][2], 'utf-8')
            wpa2Pass = cipherSuite.decrypt(encryptedWpa2Pass).decode('utf-8')
            apList = apGroupIterator(apGroupId=apGroupId, ssid=ssidInfo[0][0], wpa2Pass=wpa2Pass, vlan=ssidInfo[0][1], bridgeGroup=ssidInfo[0][3], radioSub=ssidInfo[0][4], gigaSub=ssidInfo[0][5])
            startTime = time.time()
            task = processor(operation=scout_ssid.scoutCreateSsid24, apInfo=apList)
            endTime = time.time() - startTime
            status = "Deployment of 2.4GHz SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apGroupName)
            completionTime = printCompletionTime(endTime)
            return redirect(url_for('cardinal_ssid_ops_bp.deploySsid24GhzGroup', status=status))

@cardinal_ssid_ops.route("/deploy-ssid-24ghz-radius-group", methods=["GET", "POST"])
def deploySsid24GhzRadiusGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz_radius")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-24ghz-radius-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_24ghz_radius")
            encryptedSharedSecret = bytes(ssidInfo[0][6], 'utf-8')
            sharedSecret = cipherSuite.decrypt(encryptedSharedSecret).decode('utf-8')
            apList = apGroupIterator(apGroupId=apGroupId, ssid=ssidInfo[0][0], vlan=ssidInfo[0][1], bridgeGroup=ssidInfo[0][2], radioSub=ssidInfo[0][3], gigaSub=ssidInfo[0][4], radiusIp=ssidInfo[0][5], sharedSecret=sharedSecret, authPort=ssidInfo[0][7], acctPort=ssidInfo[0][8], radiusTimeout=ssidInfo[0][9], radiusGroup=ssidInfo[0][10], methodList=ssidInfo[0][11])
            startTime = time.time()
            task = processor(operation=scout_ssid.scoutCreateSsid24Radius, apInfo=apList)
            endTime = time.time() - startTime
            status = "Deployment of 2.4GHz RADIUS SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apGroupName)
            completionTime = printCompletionTime(endTime)
            return redirect(url_for('cardinal_ssid_ops_bp.deploySsid24GhzRadiusGroup', status=status))

@cardinal_ssid_ops.route("/deploy-ssid-5ghz", methods=["GET", "POST"])
def deploySsid5Ghz():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-5ghz.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('cardinal_auth_bp.index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_5ghz")
            encryptedWpa2Pass = bytes(ssidInfo[0][2], 'utf-8')
            wpa2Pass = cipherSuite.decrypt(encryptedWpa2Pass).decode('utf-8')
            checkSsidRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_5ghz", action="test")
            if checkSsidRelationship:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                for info in apInfo:
                    apIp = info[0]
                    apSshUsername = info[1]
                    encryptedSshPassword = bytes(info[2], 'utf-8')
                    apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
                scout_ssid.scoutCreateSsid5(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssidInfo[0][0], vlan=ssidInfo[0][1], wpa2Pass=wpa2Pass, bridgeGroup=ssidInfo[0][3], radioSub=ssidInfo[0][4], gigaSub=ssidInfo[0][5])
                commitRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_5ghz", action="commit")
                status = "Deployment of 5GHz SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apName)
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid5Ghz', status=status))
            else:
                conn.close()
                status = "5GHz SSID {0} is already deployed on {1}".format(ssidInfo[0][0], apName)
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid5Ghz', status=status))

@cardinal_ssid_ops.route("/deploy-ssid-5ghz-radius", methods=["GET", "POST"])
def deploySsid5GhzRadius():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz_radius")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-5ghz-radius.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_5ghz_radius")
            encryptedSharedSecret = bytes(ssidInfo[0][6], 'utf-8')
            sharedSecret = cipherSuite.decrypt(encryptedSharedSecret).decode('utf-8')
            checkSsidRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_5ghz_radius", action="test")
            if checkSsidRelationship:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                for info in apInfo:
                    apIp = info[0]
                    apSshUsername = info[1]
                    encryptedSshPassword = bytes(info[2], 'utf-8')
                    apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
                scout_ssid.scoutCreateSsid5Radius(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssidInfo[0][0], vlan=ssidInfo[0][1], bridgeGroup=ssidInfo[0][2], radioSub=ssidInfo[0][3], gigaSub=ssidInfo[0][4], radiusIp=ssidInfo[0][5], sharedSecret=sharedSecret, authPort=ssidInfo[0][7], acctPort=ssidInfo[0][8], radiusTimeout=ssidInfo[0][9], radiusGroup=ssidInfo[0][10], methodList=ssidInfo[0][11])
                commitRelationship = ssidCheck(apId=apId, ssidId=ssidId, ssidType="ssid_5ghz_radius", action="commit")
                status = "Deployment of 5GHz RADIUS SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apName)
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid5GhzRadius', status=status))
            else:
                conn.close()
                status = "5GHz RADIUS SSID {0} is already deployed on {1}".format(ssidInfo[0][0], apName)
                return redirect(url_for('cardinal_ssid_ops_bp.deploySsid5GhzRadius', status=status))

@cardinal_ssid_ops.route("/deploy-ssid-5ghz-group", methods=["GET", "POST"])
def deploySsid5GhzGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-5ghz-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_5ghz")
            encryptedWpa2Pass = bytes(ssidInfo[0][2], 'utf-8')
            wpa2Pass = cipherSuite.decrypt(encryptedWpa2Pass).decode('utf-8')
            apList = apGroupIterator(apGroupId=apGroupId, ssid=ssidInfo[0][0], wpa2Pass=wpa2Pass, vlan=ssidInfo[0][1], bridgeGroup=ssidInfo[0][3], radioSub=ssidInfo[0][4], gigaSub=ssidInfo[0][5])
            startTime = time.time()
            task = processor(operation=scout_ssid.scoutCreateSsid5, apInfo=apList)
            endTime = time.time() - startTime
            status = "Deployment of 5GHz SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apGroupName)
            completionTime = printCompletionTime(endTime)
            return redirect(url_for('cardinal_ssid_ops_bp.deploySsid5GhzGroup', status=status))

@cardinal_ssid_ops.route("/deploy-ssid-5ghz-radius-group", methods=["GET", "POST"])
def deploySsid5GhzRadiusGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            deploySsidCursor = conn.cursor()
            deploySsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz_radius")
            ssids = deploySsidCursor.fetchall()
            deploySsidCursor.close()
            conn.close()
            return render_template("deploy-ssid-5ghz-radius-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            ssidInfo = getSsidInfo(ssidId=ssidId, ssidType="ssid_5ghz_radius")
            encryptedSharedSecret = bytes(ssidInfo[0][6], 'utf-8')
            sharedSecret = cipherSuite.decrypt(encryptedSharedSecret).decode('utf-8')
            apList = apGroupIterator(apGroupId=apGroupId, ssid=ssidInfo[0][0], vlan=ssidInfo[0][1], bridgeGroup=ssidInfo[0][2], radioSub=ssidInfo[0][3], gigaSub=ssidInfo[0][4], radiusIp=ssidInfo[0][5], sharedSecret=sharedSecret, authPort=ssidInfo[0][7], acctPort=ssidInfo[0][8], radiusTimeout=ssidInfo[0][9], radiusGroup=ssidInfo[0][10], methodList=ssidInfo[0][11])
            startTime = time.time()
            task = processor(operation=scout_ssid.scoutCreateSsid5Radius, apInfo=apList)
            endTime = time.time() - startTime
            status = "Deployment of 5GHz SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssidInfo[0][0], apGroupName)
            completionTime = printCompletionTime(endTime)
            return redirect(url_for('cardinal_ssid_ops_bp.deploySsid5GhzRadiusGroup', status=status))

@cardinal_ssid_ops.route("/remove-ssid-24ghz", methods=["GET", "POST"])
def removeSsid24Ghz():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-24ghz.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            try:
                checkSsidRelationship = conn.cursor()
                checkSsidRelationship.execute("DELETE FROM ssids_24ghz_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                checkSsidRelationship.close()
            except MySQLdb.Error as e:
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24Ghz', status=e))
            else:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                ssidInfoCursor = conn.cursor()
                ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = %s", [ssidId])
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
                status = "Removal of 2.4GHz SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssid,apName)
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24Ghz', status=status))

@cardinal_ssid_ops.route("/remove-ssid-24ghz-radius", methods=["GET", "POST"])
def removeSsid24GhzRadius():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz_radius")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-24ghz-radius.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            try:
                checkSsidRelationship = conn.cursor()
                checkSsidRelationship.execute("DELETE FROM ssids_24ghz_radius_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                checkSsidRelationship.close()
            except MySQLdb.Error as e:
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24GhzRadius', status=e))
            else:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                ssidInfoCursor = conn.cursor()
                ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [ssidId])
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
                status = "Removal of 2.4GHz RADIUS SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssid,apName)
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24GhzRadius', status=status))

@cardinal_ssid_ops.route("/remove-ssid-24ghz-group", methods=["GET", "POST"])
def removeSsid24GhzGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-24ghz-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            apGroupCheck = conn.cursor()
            apGroupCheck.execute("SELECT ap_id FROM access_points WHERE ap_group_id = %s", [apGroupId])
            apIdsSql = apGroupCheck.fetchall()
            apGroupCheck.close()
            apIds = []
            for value in apIdsSql:
                apIds.append(value[0])
            for apId in apIds:
                try:
                    checkSsidRelationship = conn.cursor()
                    checkSsidRelationship.execute("DELETE FROM ssids_24ghz_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                    checkSsidRelationship.close()
                except MySQLdb.Error as e:
                    return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24GhzGroup', status=e))
                else:
                    apInfoCursor = conn.cursor()
                    apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                    apInfo = apInfoCursor.fetchall()
                    apInfoCursor.close()
                    ssidInfoCursor = conn.cursor()
                    ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = %s", [ssidId])
                    ssidInfo = ssidInfoCursor.fetchall()
                    ssidInfoCursor.close()
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
                    conn.commit()
            conn.close()
            status = "Removal of 2.4GHz SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssid,apGroupName)
            return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24GhzGroup', status=status))

@cardinal_ssid_ops.route("/remove-ssid-24ghz-radius-group", methods=["GET", "POST"])
def removeSsid24GhzRadiusGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz_radius")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-24ghz-radius-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            apGroupCheck = conn.cursor()
            apGroupCheck.execute("SELECT ap_id FROM access_points WHERE ap_group_id = %s", [apGroupId])
            apIdsSql = apGroupCheck.fetchall()
            apGroupCheck.close()
            apIds = []
            for value in apIdsSql:
                apIds.append(value[0])
            for apId in apIds:
                try:
                    checkSsidRelationship = conn.cursor()
                    checkSsidRelationship.execute("DELETE FROM ssids_24ghz_radius_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                    checkSsidRelationship.close()
                except MySQLdb.Error as e:
                    return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24GhzRadiusGroup', status=e))
                else:
                    apInfoCursor = conn.cursor()
                    apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                    apInfo = apInfoCursor.fetchall()
                    apInfoCursor.close()
                    ssidInfoCursor = conn.cursor()
                    ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [ssidId])
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
                    conn.commit()
            conn.close()
            status = "Removal of 2.4GHz RADIUS SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssid,apGroupName)
            return redirect(url_for('cardinal_ssid_ops_bp.removeSsid24GhzRadiusGroup', status=status))

@cardinal_ssid_ops.route("/remove-ssid-5ghz", methods=["GET", "POST"])
def removeSsid5Ghz():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-5ghz.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            try:
                checkSsidRelationship = conn.cursor()
                checkSsidRelationship.execute("DELETE FROM ssids_5ghz_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                checkSsidRelationship.close()
            except MySQLdb.Error as e:
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5Ghz', status=e))
            else:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                ssidInfoCursor = conn.cursor()
                ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz WHERE ap_ssid_id = %s", [ssidId])
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
                scout_ssid.scoutDeleteSsid5(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
                status = "Removal of 5GHz SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssid,apName)
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5Ghz', status=status))

@cardinal_ssid_ops.route("/remove-ssid-5ghz-radius", methods=["GET", "POST"])
def removeSsid5GhzRadius():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz_radius")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-5ghz-radius.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apId = session.get('apId')
            apName = session.get('apName')
            try:
                checkSsidRelationship = conn.cursor()
                checkSsidRelationship.execute("DELETE FROM ssids_5ghz_radius_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                checkSsidRelationship.close()
            except MySQLdb.Error as e:
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5GhzRadius', status=e))
            else:
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                ssidInfoCursor = conn.cursor()
                ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [ssidId])
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
                scout_ssid.scoutDeleteSsid5(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
                status = "Removal of 5GHz RADIUS SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssid,apName)
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5GhzRadius', status=status))

@cardinal_ssid_ops.route("/remove-ssid-5ghz-group", methods=["GET", "POST"])
def removeSsid5GhzGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-5ghz-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            apGroupCheck = conn.cursor()
            apGroupCheck.execute("SELECT ap_id FROM access_points WHERE ap_group_id = %s", [apGroupId])
            apIdsSql = apGroupCheck.fetchall()
            apGroupCheck.close()
            apIds = []
            for value in apIdsSql:
                apIds.append(value[0])
            for apId in apIds:
                try:
                    checkSsidRelationship = conn.cursor()
                    checkSsidRelationship.execute("DELETE FROM ssids_5ghz_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                    checkSsidRelationship.close()
                except MySQLdb.Error as e:
                    return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5GhzGroup', status=e))
                else:
                    apInfoCursor = conn.cursor()
                    apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                    apInfo = apInfoCursor.fetchall()
                    apInfoCursor.close()
                    ssidInfoCursor = conn.cursor()
                    ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz WHERE ap_ssid_id = %s", [ssidId])
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
                    scout_ssid.scoutDeleteSsid5(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
                    conn.commit()
            conn.close()
            status = "Removal of 5GHz SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssid,apGroupName)
            return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5GhzGroup', status=status))

@cardinal_ssid_ops.route("/remove-ssid-5ghz-radius-group", methods=["GET", "POST"])
def removeSsid5GhzRadiusGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            removeSsidCursor = conn.cursor()
            removeSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz_radius")
            ssids = removeSsidCursor.fetchall()
            removeSsidCursor.close()
            conn.close()
            return render_template("remove-ssid-5ghz-radius-group.html", status=status, ssids=ssids)
        else:
            return redirect(url_for('index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            conn = cardinalSql()
            ssidId = request.form["ssid_id"]
            apGroupId = session.get('apGroupId')
            apGroupName = session.get('apGroupName')
            apGroupCheck = conn.cursor()
            apGroupCheck.execute("SELECT ap_id FROM access_points WHERE ap_group_id = %s", [apGroupId])
            apIdsSql = apGroupCheck.fetchall()
            apGroupCheck.close()
            apIds = []
            for value in apIdsSql:
                apIds.append(value[0])
            for apId in apIds:
                try:
                    checkSsidRelationship = conn.cursor()
                    checkSsidRelationship.execute("DELETE FROM ssids_5ghz_radius_deployed WHERE ap_id = %s AND ssid_id = %s", (apId,ssidId))
                    checkSsidRelationship.close()
                except MySQLdb.Error as e:
                    return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5GhzRadiusGroup', status=e))
                else:
                    apInfoCursor = conn.cursor()
                    apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = %s", [apId])
                    apInfo = apInfoCursor.fetchall()
                    apInfoCursor.close()
                    ssidInfoCursor = conn.cursor()
                    ssidInfoCursor.execute("SELECT ap_ssid_name, ap_ssid_vlan, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [ssidId])
                    ssidInfo = ssidInfoCursor.fetchall()
                    for ssidData in ssidInfo:
                        ssid = ssidData[0]
                        vlan = ssidData[1]
                        radioSub = ssidData[2]
                        gigaSub = ssidData[3]
                    for info in apInfo:
                        apIp = info[0]
                        apSshUsername = info[1]
                        encryptedSshPassword = bytes(info[2], 'utf-8')
                        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
                    scout_ssid.scoutDeleteSsid5(ip=apIp, username=apSshUsername, password=apSshPassword, ssid=ssid, vlan=vlan, radioSub=radioSub, gigaSub=gigaSub)
                    conn.commit()
            conn.close()
            status = "Removal of 5GHz RADIUS SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssid,apGroupName)
            return redirect(url_for('cardinal_ssid_ops_bp.removeSsid5GhzRadiusGroup', status=status))
