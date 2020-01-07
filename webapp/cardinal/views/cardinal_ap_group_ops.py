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

@cardinal_ap_group_ops.route("/manage-ap-tftp-backup-group", methods=["GET"])
def manageApTftpBackupGroup():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("manage-ap-tftp-backup-group.html", status=status)

@cardinal_ap_group_ops.route("/do-ap-tftp-backup-group", methods=["POST"])
def doApTftpBackupGroup():
    if request.method == 'POST':
        conn = cardinalSql()
        apGroupId = session.get("apGroupId")
        apGroupName = session.get("apGroupName")
        tftpIp = request.form["tftp_ip"]
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            encryptedSshPassword = bytes(info[3], 'utf-8')
            apSshPassword = cipherSuite.decrypt(encryptedSshPassword).decode('utf-8')
            scout_sys.scoutTftpBackup(ip=apIp, username=apSshUsername, password=apSshPassword, tftpIp=tftpIp)
        status = "Config Backup for AP Group {} Successfully Initiated!".format(apGroupName)
        conn.close()
        return redirect(url_for('cardinal_ap_group_ops_bp.manageApTftpBackupGroup', status=status))

