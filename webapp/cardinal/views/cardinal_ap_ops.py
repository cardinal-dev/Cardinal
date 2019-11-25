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

cardinal_ap_ops = Blueprint('cardinal_ap_ops_bp', __name__)

@cardinal_ap_ops.route("/config-ap-ip", methods=["GET"])
def configApIp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-ip.html", status=status)

@cardinal_ap_ops.route("/do-config-ap-ip", methods=["POST"])
def doConfigApIp():
    if request.method == 'POST':
        apId = session.get('apId')
        apNewIp = request.form["ap_new_ip"]
        apSubnetMask = request.form["ap_subnetmask"]
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutChangeIp(ip=apIp, username=apSshUsername, password=apSshPassword, newIp=apNewIp, subnetMask=apSubnetMask)
        status = "{}'s IP was successfully updated!".format(apName)
        changeApIpCursor = conn.cursor()
        changeApIpCursor.execute("UPDATE access_points SET ap_ip = '{0}' WHERE ap_id = '{1}'".format(apNewIp,apId))
        changeApIpCursor.close()
        conn.commit()
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApIp', status=status))

@cardinal_ap_ops.route("/config-ap-name", methods=["GET"])
def configApName():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-name.html", status=status)

@cardinal_ap_ops.route("/do-config-ap-name", methods=["POST"])
def doConfigApName():
    if request.method == 'POST':
        apId = session.get('apId')
        apNewName = request.form["ap_name"]
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutChangeName(ip=apIp, username=apSshUsername, password=apSshPassword, apName=apNewName)
        status = "AP Name Changed from {0} to {1}".format(apName,apNewName)
        changeApNameCursor = conn.cursor()
        changeApNameCursor.execute("UPDATE access_points SET ap_name = '{0}' WHERE ap_id = '{1}'".format(apNewName,apId))
        conn.commit()
        changeApNameCursor.close()
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApName', status=status))

@cardinal_ap_ops.route("/manage-ap-tftp-backup", methods=["GET"])
def manageApTftpBackup():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("manage-ap-tftp-backup.html", status=status)

@cardinal_ap_ops.route("/do-ap-tftp-backup", methods=["POST"])
def doApTftpBackup():
    if request.method == 'POST':
        apId = session.get('apId')
        tftpIp = request.form["tftp_ip"]
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutTftpBackup(ip=apIp, username=apSshUsername, password=apSshPassword, tftpIp=tftpIp)
        status = "Config Backup for {} Successfully Initiated!".format(apName)
        conn.close()
        if request.form["group_backup"] == 'True':
            apGroupId = session.get('apGroupId', None)
            apGroupName = session.get('apGroupName', None)
            tftpIp = request.form["tftp_ip"]
            conn = cardinalSql()
            apInfoCursor = conn.cursor()
            apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
            apInfo = apInfoCursor.fetchall()
            apInfoCursor.close()
            for info in apInfo:
                apGroupName = info[0]
                apIp = info[1]
                apSshUsername = info[2]
                encryptedSshPassword = bytes(info[3], 'utf-8')
                apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
                scout_sys.scoutTftpBackup(ip=apIp, username=apSshUsername, password=apSshPassword, tftpIp=tftpIp)
            status = "Config Backup for {} Successfully Initiated!".format(apGroupName)
            conn.close()
            return redirect(url_for('cardinal_ap_ops_bp.configApName', status=status))
        return redirect(url_for('manageApTftpBackup', status=status))

@cardinal_ap_ops.route("/config-ap-http", methods=["GET"])
def configApHttp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-http.html", status=status)

@cardinal_ap_ops.route("/do-enable-ap-http", methods=["POST"])
def doEnableApHttp():
    if request.method == 'POST':
        apId = session.get('apId')
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutEnableHttp(ip=apIp, username=apSshUsername, password=apSshPassword)
        status = "HTTP Server for {} Successfully Enabled!".format(apName)
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApHttp', status=status))

@cardinal_ap_ops.route("/do-disable-ap-http", methods=["POST"])
def doDisableApHttp():
    if request.method == 'POST':
        apId = session.get('apId')
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutDisableHttp(ip=apIp, username=apSshUsername, password=apSshPassword)
        status = "HTTP Server for {} Successfully Disabled".format(apName)
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApHttp', status=status))

@cardinal_ap_ops.route("/config-ap-radius", methods=["GET"])
def configApRadius():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-radius.html", status=status)

@cardinal_ap_ops.route("/do-enable-ap-radius", methods=["POST"])
def doEnableApRadius():
    if request.method == 'POST':
        apId = session.get('apId')
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutEnableRadius(ip=apIp, username=apSshUsername, password=apSshPassword)
        status = "RADIUS for {} Successfully Enabled!".format(apName)
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApRadius', status=status))

@cardinal_ap_ops.route("/do-disable-ap-radius", methods=["POST"])
def doDisableApRadius():
    if request.method == 'POST':
        apId = session.get('apId')
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutDisableRadius(ip=apIp, username=apSshUsername, password=apSshPassword)
        status = "RADIUS Server for {} Successfully Disabled!".format(apName)
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApRadius', status=status))

@cardinal_ap_ops.route("/config-ap-snmp", methods=["GET"])
def configApSnmp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-snmp.html", status=status)

@cardinal_ap_ops.route("/do-enable-ap-snmp", methods=["POST"])
def doEnableApSnmp():
    if request.method == 'POST':
        apId = session.get('apId')
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutEnableSnmp(ip=apIp, username=apSshUsername, password=apSshPassword)
        status = "SNMP for {} Successfully Enabled!".format(apName)
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApSnmp', status=status))

@cardinal_ap_ops.route("/do-disable-ap-snmp", methods=["POST"])
def doDisableApSnmp():
    if request.method == 'POST':
        apId = session.get('apId')
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
        apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
        scout_sys.scoutDisableSnmp(ip=apIp, username=apSshUsername, password=apSshPassword)
        status = "SNMP Server for {} Successfully Disabled!".format(apName)
        conn.close()
        return redirect(url_for('cardinal_ap_ops_bp.configApSnmp', status=status))
