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
from cardinal.system.cardinal_sys import cipherSuite
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from scout import scout_sys

cardinal_ap_group_ops = Blueprint('cardinal_ap_group_ops_bp', __name__)

@cardinal_ap_group_ops.route("/config-ap-group-tftp-backup", methods=["GET", "POST"])
def apGroupTftpBackup():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("config-ap-group-tftp-backup.html", status=status)
    elif request.method == 'POST':
        conn = cardinalSql()
        apGroupId = session.get("apGroupId")
        apGroupName = session.get("apGroupName")
        tftpIp = request.form["tftp_ip"]
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apIp = info[0]
            apSshUsername = info[1]
            encryptedSshPassword = bytes(info[2], 'utf-8')
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
            scout_sys.scoutTftpBackup(ip=apIp, username=apSshUsername, password=apSshPassword, tftpIp=tftpIp)
        status = "Config Backup for AP Group {} Successfully Initiated!".format(apGroupName)
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApTftpBackup', status=status))

@cardinal_ap_group_ops.route("/config-ap-group-http", methods=["GET"])
def configApHttp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-group-http.html", status=status)

@cardinal_ap_group_ops.route("/enable-ap-group-http", methods=["POST"])
def enableApHttp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
    apInfo = apInfoCursor.fetchall()
    apInfoCursor.close()
    for info in apInfo:
        apIp = info[0]
        apSshUsername = info[1]
        encryptedSshPassword = bytes(info[2], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutEnableHttp(ip=apIp, username=apSshUsername, password=apSshPassword)
    status = "HTTP Server for AP Group {} Successfully Enabled!".format(apGroupName)
    conn.close()
    return redirect(url_for('cardinal_ap_group_ops_bp.configApHttp', status=status))

@cardinal_ap_group_ops.route("/disable-ap-group-http", methods=["POST"])
def disableApHttp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
    apInfo = apInfoCursor.fetchall()
    apInfoCursor.close()
    for info in apInfo:
        apIp = info[0]
        apSshUsername = info[1]
        encryptedSshPassword = bytes(info[2], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutDisableHttp(ip=apIp, username=apSshUsername, password=apSshPassword)
    status = "HTTP Server for AP Group {} Successfully Disabled!".format(apGroupName)
    conn.close()
    return redirect(url_for('cardinal_ap_group_ops_bp.configApHttp', status=status))

@cardinal_ap_group_ops.route("/config-ap-group-radius", methods=["GET"])
def configApRadius():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-group-radius.html", status=status)

@cardinal_ap_group_ops.route("/enable-ap-group-radius", methods=["POST"])
def enableApRadius():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
    apInfo = apInfoCursor.fetchall()
    apInfoCursor.close()
    for info in apInfo:
        apIp = info[0]
        apSshUsername = info[1]
        encryptedSshPassword = bytes(info[2], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutEnableRadius(ip=apIp, username=apSshUsername, password=apSshPassword)
    status = "RADIUS for AP Group {} Successfully Enabled!".format(apGroupName)
    conn.close()
    return redirect(url_for('cardinal_ap_group_ops_bp.configApRadius', status=status))

@cardinal_ap_group_ops.route("/disable-ap-group-radius", methods=["POST"])
def disableApRadius():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
    apInfo = apInfoCursor.fetchall()
    apInfoCursor.close()
    for info in apInfo:
        apIp = info[0]
        apSshUsername = info[1]
        encryptedSshPassword = bytes(info[2], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutDisableRadius(ip=apIp, username=apSshUsername, password=apSshPassword)
    status = "RADIUS Server for AP Group {} Successfully Disabled!".format(apGroupName)
    conn.close()
    return redirect(url_for('cardinal_ap_group_ops_bp.configApRadius', status=status))

@cardinal_ap_group_ops.route("/config-ap-group-snmp", methods=["GET"])
def configApSnmp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-group-snmp.html", status=status)

@cardinal_ap_group_ops.route("/enable-ap-group-snmp", methods=["POST"])
def enableApSnmp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password,ap_snmp FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
    apInfo = apInfoCursor.fetchall()
    apInfoCursor.close()
    for info in apInfo:
        apIp = info[0]
        apSshUsername = info[1]
        encryptedSshPassword = bytes(info[2], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        encryptedSnmp = bytes(info[3], 'utf-8')
        apSnmp = cipherSuite.decrypt(encryptedSnmp).decode('utf-8')
        scout_sys.scoutEnableSnmp(ip=apIp, username=apSshUsername, password=apSshPassword, snmp=apSnmp)
    status = "SNMP for AP Group {} Successfully Enabled!".format(apGroupName)
    conn.close()
    return redirect(url_for('cardinal_ap_group_ops_bp.configApSnmp', status=status))

@cardinal_ap_group_ops.route("/disable-ap-group-snmp", methods=["POST"])
def disableApSnmp():
    apGroupId = session.get('apGroupId')
    apGroupName = session.get('apGroupName')
    conn = cardinalSql()
    apInfoCursor = conn.cursor()
    apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
    apInfo = apInfoCursor.fetchall()
    apInfoCursor.close()
    for info in apInfo:
        apIp = info[0]
        apSshUsername = info[1]
        encryptedSshPassword = bytes(info[2], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutDisableSnmp(ip=apIp, username=apSshUsername, password=apSshPassword)
    status = "SNMP Server for AP Group {} Successfully Disabled!".format(apGroupName)
    conn.close()
    return redirect(url_for('cardinal_ap_group_ops_bp.configApSnmp', status=status))
