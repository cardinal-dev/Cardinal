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

import time
from cardinal.system.cardinal_sys import apGroupIterator
from cardinal.system.cardinal_sys import printCompletionTime
from cardinal.system.cardinal_sys import cipherSuite
from cardinal.system.cardinal_sys import processor
from cardinal.system.cardinal_sys import msgAuthFailed
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from scout import scout_sys

cardinal_ap_group_ops = Blueprint('cardinal_ap_group_ops_bp', __name__)

@cardinal_ap_group_ops.route("/get-ap-group-tftp-backup", methods=["GET", "POST"])
def configApTftpBackup():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            completionTime = request.args.get('completionTime')
            return render_template("config-ap-group-tftp-backup.html", status=status, completionTime=completionTime)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            apGroupId = session.get("apGroupId")
            apGroupName = session.get("apGroupName")
            if apGroupId is None:
                apGroupId = request.form["ap_group_id"]
            tftpIp = request.form["tftp_ip"]
            apList = apGroupIterator(apGroupId=apGroupId, tftpIp=tftpIp)
            startTime = time.time()
            task = processor(operation=scout_sys.scoutTftpBackup, apInfo=apList)
            endTime = time.time() - startTime
            status = "INFO: Config Backup for AP Group {} Successfully Initiated!".format(apGroupName)
            completionTime = printCompletionTime(endTime)
            return redirect(url_for('cardinal_ap_group_ops_bp.configApTftpBackup', status=status, completionTime=completionTime))
        else:
            return msgAuthFailed, 401

@cardinal_ap_group_ops.route("/config-ap-group-http", methods=["GET"])
def configApHttp():
    if session.get("username") is not None:
        completionTime = request.args.get('completionTime')
        status = request.args.get('status')
        return render_template("config-ap-group-http.html", status=status, completionTime=completionTime)
    else:
        return msgAuthFailed, 401

@cardinal_ap_group_ops.route("/enable-ap-group-http", methods=["POST"])
def enableApHttp():
    if session.get("username") is not None:
        apGroupId = session.get('apGroupId')
        apGroupName = session.get('apGroupName')
        if apGroupId is None:
            apGroupId = request.form["ap_group_id"]
        apList = apGroupIterator(apGroupId=apGroupId)
        startTime = time.time()
        task = processor(operation=scout_sys.scoutEnableHttp, apInfo=apList)
        endTime = time.time() - startTime
        status = "INFO: HTTP Server for AP Group {} Successfully Enabled!".format(apGroupName)
        completionTime = printCompletionTime(endTime)
        return redirect(url_for('cardinal_ap_group_ops_bp.configApHttp', status=status, completionTime=completionTime))
    else:
        return msgAuthFailed, 401

@cardinal_ap_group_ops.route("/disable-ap-group-http", methods=["POST"])
def disableApHttp():
    if session.get("username") is not None:
        apGroupId = session.get('apGroupId')
        apGroupName = session.get('apGroupName')
        if apGroupId is None:
            apGroupId = request.form["ap_group_id"]
        apList = apGroupIterator(apGroupId=apGroupId)
        startTime = time.time()
        task = processor(operation=scout_sys.scoutDisableHttp, apInfo=apList)
        endTime = time.time() - startTime
        status = "INFO: HTTP Server for AP Group {} Successfully Disabled!".format(apGroupName)
        completionTime = printCompletionTime(endTime)
        return redirect(url_for('cardinal_ap_group_ops_bp.configApHttp', status=status, completionTime=completionTime))
    else:
        return msgAuthFailed, 401

@cardinal_ap_group_ops.route("/config-ap-group-snmp", methods=["GET"])
def configApSnmp():
    if session.get("username") is not None:
        completionTime = request.args.get('completionTime')
        status = request.args.get('status')
        return render_template("config-ap-group-snmp.html", status=status, completionTime=completionTime)
    else:
        return msgAuthFailed, 401

@cardinal_ap_group_ops.route("/enable-ap-group-snmp", methods=["POST"])
def enableApSnmp():
    if session.get("username") is not None:
        apGroupId = session.get('apGroupId')
        apGroupName = session.get('apGroupName')
        if apGroupId is None:
            apGroupId = request.form["ap_group_id"]
        apList = apGroupIterator(apGroupId=apGroupId, snmp="True")
        startTime = time.time()
        task = processor(operation=scout_sys.scoutEnableSnmp, apInfo=apList)
        endTime = time.time() - startTime
        status = "INFO: SNMP Server for AP Group {} Successfully Enabled!".format(apGroupName)
        completionTime = printCompletionTime(endTime)
        return redirect(url_for('cardinal_ap_group_ops_bp.configApSnmp', status=status, completionTime=completionTime))
    else:
        return msgAuthFailed, 401

@cardinal_ap_group_ops.route("/disable-ap-group-snmp", methods=["POST"])
def disableApSnmp():
    if session.get("username") is not None:
        apGroupId = session.get('apGroupId')
        apGroupName = session.get('apGroupName')
        if apGroupId is None:
            apGroupId = request.form["ap_group_id"]
        apList = apGroupIterator(apGroupId=apGroupId)
        startTime = time.time()
        task = processor(operation=scout_sys.scoutDisableSnmp, apInfo=apList)
        endTime = time.time() - startTime
        status = "INFO: SNMP Server for AP Group {} Successfully Disabled!".format(apGroupName)
        completionTime = printCompletionTime(endTime)
        return redirect(url_for('cardinal_ap_group_ops_bp.configApSnmp', status=status, completionTime=completionTime))
    else:
        return msgAuthFailed, 401
