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
from cardinal.system.cardinal_fetch import gatherApInfo
from cardinal.system.cardinal_sys import cardinalSql
from cardinal.system.cardinal_sys import cipherSuite
from cardinal.system.cardinal_sys import getApInfo
from cardinal.system.cardinal_sys import msgAuthFailed
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from scout import sys

cardinal_ap_ops = Blueprint('cardinal_ap_ops_bp', __name__)

@cardinal_ap_ops.route("/change-ap-ip", methods=["GET", "POST"])
def configApIp():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("config-ap-ip.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            apId = session.get('apId')
            if apId is None:
                apId = request.form["ap_id"]
            apNewIp = request.form["ap_new_ip"]
            apSubnetMask = request.form["ap_subnetmask"]
            apInfo = getApInfo(apId=apId)
            encryptedSshPassword = bytes(apInfo[0][3], 'utf-8')
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
            sys.scoutChangeIp(ip=apInfo[0][1], username=apInfo[0][2], password=apSshPassword, newIp=apNewIp, subnetMask=apSubnetMask)
            status = "{}'s IP was successfully updated!".format(apInfo[0][0])
            try:
                conn = cardinalSql()
                changeApIpCursor = conn.cursor()
                changeApIpCursor.execute("UPDATE access_points SET ap_ip = %s WHERE ap_id = %s", (apNewIp,apId))
                changeApIpCursor.close()
            except MySQLdb.Error as e:
                conn.close()
                return redirect(url_for('cardinal_ap_ops_bp.configApIp', status=e))
            else:
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ap_ops_bp.configApIp', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ap_ops.route("/change-ap-name", methods=["GET", "POST"])
def configApName():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("config-ap-name.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            apId = session.get('apId')
            if apId is None:
                apId = request.form["ap_id"]
            apNewName = request.form["ap_name"]
            apInfo = getApInfo(apId=apId)
            encryptedSshPassword = bytes(apInfo[0][3], 'utf-8')
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
            sys.scoutChangeName(ip=apInfo[0][1], username=apInfo[0][2], password=apSshPassword, apName=apNewName)
            status = "AP Name Changed from {0} to {1}".format(apInfo[0][0],apNewName)
            try:
                conn = cardinalSql()
                changeApNameCursor = conn.cursor()
                changeApNameCursor.execute("UPDATE access_points SET ap_name = %s WHERE ap_id = %s", (apNewName,apId))
                changeApNameCursor.close()
            except MySQLdb.Error as e:
                conn.close()
                return redirect(url_for('cardinal_ap_ops_bp.configApName', status=e))
            else:
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ap_ops_bp.configApName', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ap_ops.route("/get-ap-tftp-backup", methods=["GET", "POST"])
def configApTftpBackup():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("config-ap-tftp-backup.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            apId = session.get('apId')
            if apId is None:
                apId = request.form["ap_id"]
            tftpIp = request.form["tftp_ip"]
            apInfo = getApInfo(apId=apId)
            encryptedSshPassword = bytes(apInfo[0][3], 'utf-8')
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
            sys.scoutTftpBackup(ip=apInfo[0][1], username=apInfo[0][2], password=apSshPassword, tftpIp=tftpIp)
            status = "Config Backup for {} Successfully Initiated!".format(apInfo[0][0])
            return redirect(url_for('cardinal_ap_ops_bp.configApTftpBackup', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ap_ops.route("/get-ap-info", methods=["GET", "POST"])
def fetchApInfo():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("fetch-ap-info.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            apId = session.get('apId')
            if apId is None:
                apId = request.form['ap_id']
            status = gatherApInfo(apId)
            return redirect(url_for('cardinal_ap_ops_bp.fetchApInfo', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ap_ops.route("/config-ap-http", methods=["GET"])
def configApHttp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-http.html", status=status)
    else:
        return msgAuthFailed, 401

@cardinal_ap_ops.route("/enable-ap-http", methods=["POST"])
def enableApHttp():
    if session.get("username") is not None:
        apId = session.get('apId')
        if apId is None:
            apId = request.form['ap_id']
        apInfo = getApInfo(apId=apId)
        encryptedSshPassword = bytes(apInfo[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        sys.scoutEnableHttp(ip=apInfo[0][1], username=apInfo[0][2], password=apSshPassword)
        status = "HTTP Server for {} Successfully Enabled!".format(apInfo[0][0])
        return redirect(url_for('cardinal_ap_ops_bp.configApHttp', status=status))
    else:
        return msgAuthFailed, 401

@cardinal_ap_ops.route("/disable-ap-http", methods=["POST"])
def disableApHttp():
    if session.get("username") is not None:
        apId = session.get('apId')
        if apId is None:
            apId = request.form["ap_id"]
        apInfo = getApInfo(apId=apId)
        encryptedSshPassword = bytes(apInfo[0][3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        sys.scoutDisableHttp(ip=apInfo[0][1], username=apInfo[0][2], password=apSshPassword)
        status = "HTTP Server for {} Successfully Disabled".format(apInfo[0][0])
        return redirect(url_for('cardinal_ap_ops_bp.configApHttp', status=status))
    else:
        return msgAuthFailed, 401

@cardinal_ap_ops.route("/config-ap-snmp", methods=["GET"])
def configApSnmp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-snmp.html", status=status)
    else:
        return msgAuthFailed, 401

@cardinal_ap_ops.route("/enable-ap-snmp", methods=["POST"])
def enableApSnmp():
    if session.get("username") is not None:
        apId = session.get('apId')
        if apId is None:
            apId = request.form["ap_id"]
        apInfo = getApInfo(apId=apId)
        encryptedSshPassword = bytes(apInfo[0][3], 'utf-8')
        encryptedSnmp = bytes(apInfo[0][4], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        apSnmp = cipherSuite.decrypt(encryptedSnmp).decode('utf-8')
        sys.scoutEnableSnmp(ip=apInfo[0][1], username=apInfo[0][2], password=apSshPassword, snmp=apSnmp)
        status = "SNMP for {} Successfully Enabled!".format(apInfo[0][0])
        return redirect(url_for('cardinal_ap_ops_bp.configApSnmp', status=status))
    else:
        return msgAuthFailed, 401

@cardinal_ap_ops.route("/disable-ap-snmp", methods=["POST"])
def disableApSnmp():
    if session.get("username") is not None:
        apId = session.get('apId')
        if apId is None:
            apId = request.form["ap_id"]
        apInfo = getApInfo(apId=apId)
        encryptedSshPassword = bytes(apInfo[0][3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        sys.scoutDisableSnmp(ip=apInfo[0][1], username=apInfo[0][2], password=apSshPassword)
        status = "SNMP Server for {} Successfully Disabled!".format(apInfo[0][0])
        return redirect(url_for('cardinal_ap_ops_bp.configApSnmp', status=status))
    else:
        return msgAuthFailed, 401
