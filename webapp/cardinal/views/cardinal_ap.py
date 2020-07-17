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
from cardinal.system.cardinal_sys import cardinalSql
from cardinal.system.cardinal_sys import cipherSuite
from cardinal.system.cardinal_sys import msgResourceAdded
from cardinal.system.cardinal_sys import msgResourceDeleted
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_ap = Blueprint('cardinal_ap_bp', __name__)

@cardinal_ap.route("/add-ap", methods=["GET", "POST"])
def addAp():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            conn = cardinalSql()
            apGroupCursor = conn.cursor()
            apGroupCursor.execute("SELECT ap_group_id,ap_group_name FROM access_point_groups")
            apGroups = apGroupCursor.fetchall()
            apGroupCursor.close()
            conn.close()
            return render_template("add-ap.html", status=status, apGroups=apGroups)
        else:
            return redirect(url_for('cardinal_auth_bp.index'), 401)
    elif request.method == 'POST':
        if session.get("username") is not None:
            apName = request.form["ap_name"]
            apIp = request.form["ap_ip"]
            apSshUsername = request.form["ssh_username"]
            apSshPassword = bytes(request.form["ssh_password"], 'utf-8')
            apGroupId = request.form["group_id"]
            if len(apGroupId) <= 0:
                apGroupId = None
            apSnmp = bytes(request.form["ap_snmp"], 'utf-8')
            status = msgResourceAdded(resource=apName)
            encryptedSshPassword = cipherSuite.encrypt(apSshPassword).decode('utf-8')
            encryptedSnmpCommunity = cipherSuite.encrypt(apSnmp).decode('utf-8')
            conn = cardinalSql()
            try:
                if apGroupId is None:
                    addApCursor = conn.cursor()
                    addApCursor.execute("INSERT INTO access_points (ap_name, ap_ip, ap_ssh_username, ap_ssh_password, ap_snmp, ap_group_id) VALUES (%s, %s, %s, %s, %s, NULL)", (apName, apIp, apSshUsername, encryptedSshPassword, encryptedSnmpCommunity))
                    addApCursor.close()
                else:
                    addApCursor = conn.cursor()
                    addApCursor.execute("INSERT INTO access_points (ap_name, ap_ip, ap_ssh_username, ap_ssh_password, ap_snmp, ap_group_id) VALUES (%s, %s, %s, %s, %s, %s)", (apName, apIp, apSshUsername, encryptedSshPassword, encryptedSnmpCommunity, apGroupId))
                    addApCursor.close()
            except MySQLdb.Error as e:
                return redirect(url_for('cardinal_ap_bp.addAp', status=e))
            else:
                conn.commit()
            conn.close()
            return redirect(url_for('cardinal_ap_bp.addAp', status=status))

@cardinal_ap.route("/delete-ap", methods=["GET", "POST"])
def deleteAp():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            conn = cardinalSql()
            apCursor = conn.cursor()
            apCursor.execute("SELECT ap_id,ap_name FROM access_points")
            aps = apCursor.fetchall()
            apCursor.close()
            conn.close()
            return render_template("delete-ap.html", aps=aps, status=status)
        else:
            return redirect(url_for('cardinal_auth_bp.index'), 401)
    elif request.method == 'POST':
        if session.get("username") is not None:
            apId = request.form["ap_id"]
            if len(apId) <= 0:
                status = "Please select a valid access point."
                return redirect(url_for('cardinal_ap_bp.deleteAp', status=status))
            conn = cardinalSql()
            deleteApNameCursor = conn.cursor()
            deleteApNameCursor.execute("SELECT ap_name FROM access_points WHERE ap_id = %s", [apId])
            apName = deleteApNameCursor.fetchone()[0]
            deleteApNameCursor.close()
            status = msgResourceDeleted(apName)
            try:
                deleteApCursor = conn.cursor()
                deleteApCursor.execute("DELETE FROM access_points WHERE ap_id = %s", [apId])
                deleteApCursor.close()
            except MySQLdb.Error as e:
                return redirect(url_for('cardinal_ap_bp.deleteAp', status=e))
            else:
                conn.commit()
            conn.close()
            return redirect(url_for('cardinal_ap_bp.deleteAp', status=status))

@cardinal_ap.route("/manage-ap-dashboard", methods=["GET", "POST"])
def manageApDashboard():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            apCursor = conn.cursor()
            apCursor.execute("SELECT ap_id,ap_name FROM access_points")
            aps = apCursor.fetchall()
            apCursor.close()
            conn.close()
            return render_template("choose-ap-dashboard.html", aps=aps, status=status)
        else:
            return redirect(url_for('cardinal_auth_bp.index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            apId = request.form['ap_id']
            if len(apId) <= 0:
                status = "Please select a valid access point."
                return redirect(url_for('cardinal_ap_bp.manageApDashboard', status=status))
            else:
                conn = cardinalSql()
                apInfoCursor = conn.cursor()
                apInfoCursor.execute("SELECT ap_name,ap_ip,ap_total_clients,ap_bandwidth,ap_model FROM access_points WHERE ap_id = %s", [apId])
                apInfo = apInfoCursor.fetchall()
                apInfoCursor.close()
                conn.close()
                for info in apInfo:
                    apName = info[0]
                    apIp = info[1]
                    apTotalClients = info[2]
                    apBandwidth = info[3]
                    apModel = info[4]
                session['apId'] = apId
                session['apName'] = apName
                session['apIp'] = apIp
                session['apTotalClients'] = apTotalClients
                session['apBandwidth'] = apBandwidth
                session['apModel'] = apModel
                return render_template("manage-ap-dashboard.html")
