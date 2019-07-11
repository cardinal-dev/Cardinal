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
import os
import subprocess
from configparser import ConfigParser
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash

# System variables

cardinalConfig = os.environ['CARDINALCONFIG']

# Flask app intitialization

Cardinal = Flask(__name__)
Cardinal.secret_key = "SECRET_KEY_HERE"

# MySQL authentication

mysqlConfig = ConfigParser()
mysqlConfig.read("{}".format(cardinalConfig))
mysqlHost = mysqlConfig.get('cardinal', 'dbserver')
mysqlUser = mysqlConfig.get('cardinal', 'username')
mysqlPass = mysqlConfig.get('cardinal', 'password')
mysqlDb = mysqlConfig.get('cardinal', 'dbname')

def cardinalSql():
    conn = MySQLdb.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPass, db = mysqlDb)
    return conn

# Cardinal Flask routes

@Cardinal.route("/")
def index():
    if session.get("username") is not None:
        return redirect(url_for('dashboard'))
    else:
        return render_template("index.html")

@Cardinal.route("/dashboard")
def dashboard():
    if session.get("username") is not None:
        return render_template("dashboard.html")
    else:
        return redirect(url_for('index'))

@Cardinal.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = cardinalSql()
    loginCursor = conn.cursor()
    loginSql = loginCursor.execute("SELECT username,password FROM users WHERE username = '{}'".format(username))
    userInfo = loginCursor.fetchall()
    loginCursor.close()
    conn.close()
    if loginSql > 0:
        for info in userInfo:
            dbUsername = info[0]
            dbHash = info[1]
    else:
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'
    if check_password_hash(dbHash,password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    elif dbUsername is None:
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'
    else:
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'

@Cardinal.route("/logout")
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

@Cardinal.route("/add-ap", methods=["GET"])
def addAp():
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
        return redirect(url_for('index'))

@Cardinal.route("/submit-add-ap", methods=["POST"])
def submitAddAp():
    if request.method == 'POST':
        apName = request.form["ap_name"]
        apIp = request.form["ap_ip"]
        apSshUsername = request.form["ssh_username"]
        apSshPassword = request.form["ssh_password"]
        apGroupId = request.form["group_id"]
        apSnmp = request.form["ap_snmp"]
        status = "Success! {} was successfully registered!".format(apName)
        conn = cardinalSql()
        addApCursor = conn.cursor()
        addApCursor.execute("INSERT INTO access_points (ap_name, ap_ip, ap_ssh_username, ap_ssh_password, ap_snmp, ap_group_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(apName, apIp, apSshUsername, apSshPassword, apSnmp, apGroupId))
        addApCursor.close()
        conn.commit()
        conn.close()
        return redirect(url_for('addAp', status=status))

@Cardinal.route("/delete-ap", methods=["GET"])
def deleteAp():
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
        return redirect(url_for('index'))

@Cardinal.route("/submit-delete-ap", methods=["POST"])
def submitDeleteAp():
    if request.method == 'POST':
        apId = request.form["ap_id"]
        conn = cardinalSql()
        deleteApNameCursor = conn.cursor()
        deleteApNameCursor.execute("SELECT ap_name FROM access_points WHERE ap_id = '{}'".format(apId))
        apName = deleteApNameCursor.fetchone()[0]
        deleteApNameCursor.close()
        status = "Success! {} was successfully registered!".format(apName)
        deleteApCursor = conn.cursor()
        deleteApCursor.execute("DELETE FROM access_points WHERE ap_id = '{}'".format(apId))
        deleteApCursor.close()
        conn.commit()
        conn.close()
        return redirect(url_for('deleteAp', status=status))

@Cardinal.route("/add-ap-group", methods=["GET"])
def addApGroup():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("add-ap-group.html", status=status)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/submit-add-ap-group", methods=["POST"])
def submitAddApGroup():
    if request.method == 'POST':
        apGroupName = request.form["ap_group_name"]
        status = "Success! {} was successfully registered!".format(apGroupName)
        conn = cardinalSql()
        addApGroupCursor = conn.cursor()
        addApGroupCursor.execute("INSERT INTO access_point_groups (ap_group_name) VALUES ('{}')".format(apGroupName))
        addApGroupCursor.close()
        conn.commit()
        conn.close()
        return render_template('add-ap-group.html', status=status)

@Cardinal.route("/delete-ap-group", methods=["GET"])
def deleteApGroup():
    if session.get("username") is not None:
        conn = cardinalSql()
        status = request.args.get('status')
        deleteApGroupCursor = conn.cursor()
        deleteApGroupCursor.execute("SELECT ap_group_id,ap_group_name FROM access_point_groups")
        apGroups = deleteApGroupCursor.fetchall()
        deleteApGroupCursor.close()
        conn.close()
        return render_template("delete-ap-group.html", status=status, apGroups=apGroups)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/submit-delete-ap-group", methods=["POST"])
def submitDeleteApGroup():
    if request.method == 'POST':
        apGroupId = request.form["ap_group_id"]
        conn = cardinalSql()
        deleteApGroupNameCursor = conn.cursor()
        deleteApGroupNameCursor.execute("SELECT ap_group_name FROM access_point_groups WHERE ap_group_id = '{}'".format(apGroupId))
        apGroupName = deleteApGroupNameCursor.fetchone()[0]
        status = "Success! {} was successfully deleted!".format(apGroupName)
        deleteApGroupCursor = conn.cursor()
        deleteApGroupCursor.execute("DELETE FROM access_point_groups WHERE ap_group_id = '{}'".format(apGroupId))
        conn.commit()
        conn.close()
        return redirect(url_for('deleteApGroup', status=status))

@Cardinal.route("/network-tools", methods=["GET"])
def networkTools():
    if session.get("username") is not None:
        return render_template("network-tools.html")
    else:
        return redirect(url_for('index'))

@Cardinal.route("/tools-output", methods=["GET"])
def networkToolsOutput():
    if session.get("username") is not None:
        commandOutput = request.args.get("commandOutput")
        return render_template("network-tools-output.html", commandOutput=commandOutput)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/do-nmap", methods=["POST"])
def doNmap():
    if request.method == 'POST':
        ip = request.form["network_ip"]
        commandOutput = subprocess.check_output("nmap -v -A {}".format(ip), shell=True)
        return redirect(url_for('networkToolsOutput', commandOutput=commandOutput))

@Cardinal.route("/do-ping", methods=["POST"])
def doPing():
    if request.method == 'POST':
        ip = request.form["network_ip"]
        commandOutput = subprocess.check_output("ping -c 4 {}".format(ip), shell=True)
        return redirect(url_for('networkToolsOutput', commandOutput=commandOutput))

@Cardinal.route("/do-tracert", methods=["POST"])
def doTracert():
    if request.method == 'POST':
        ip = request.form["network_ip"]
        commandOutput = subprocess.check_output("traceroute {}".format(ip), shell=True)
        return redirect(url_for('networkToolsOutput', commandOutput=commandOutput))

@Cardinal.route("/do-dig", methods=["POST"])
def doDig():
    if request.method == 'POST':
        ip = request.form["network_ip"]
        commandOutput = subprocess.check_output("dig {}".format(ip), shell=True)
        return redirect(url_for('networkToolsOutput', commandOutput=commandOutput))

@Cardinal.route("/do-curl", methods=["POST"])
def doCurl():
    if request.method == 'POST':
        ip = request.form["network_ip"]
        commandOutput = subprocess.check_output("curl -I {}".format(ip), shell=True)
        return redirect(url_for('networkToolsOutput', commandOutput=commandOutput))

@Cardinal.route("/choose-ap-dashboard", methods=["GET"])
def chooseApDashboard():
    if session.get("username") is not None:
        conn = cardinalSql()
        apCursor = conn.cursor()
        apCursor.execute("SELECT ap_id,ap_name FROM access_points")
        aps = apCursor.fetchall()
        apCursor.close()
        conn.close()
        return render_template("choose-ap-dashboard.html", aps=aps)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/manage-ap-dashboard", methods=["POST"])
def manageApDashboard():
    if request.method == 'POST':
        apId = request.form["ap_id"]
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_total_clients,ap_bandwidth FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        conn.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apTotalClients = info[2]
            apBandwidth = info[3]
        session['apId'] = apId
        session['apName'] = apName
        session['apIp'] = apIp
        session['apTotalClients'] = apTotalClients
        session['apBandwidth'] = apBandwidth
        return render_template("manage-ap-dashboard.html")
    else:
        return redirect(url_for('index'))

@Cardinal.route("/choose-ap-group-dashboard", methods=["GET"])
def chooseApGroupDashboard():
    if session.get("username") is not None:
        conn = cardinalSql()
        apGroupCursor = conn.cursor()
        apGroupCursor.execute("SELECT ap_group_id,ap_group_name FROM access_point_groups")
        apGroups = apGroupCursor.fetchall()
        apGroupCursor.close()
        conn.close()
        return render_template("choose-ap-group-dashboard.html", apGroups=apGroups)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/manage-ap-group-dashboard", methods=["POST"])
def manageApGroupDashboard():
    if request.method == 'POST':
        apGroupId = request.form["ap_group_id"]
        conn = cardinalSql()
        apGroupInfoCursor = conn.cursor()
        apGroupInfoCursor.execute("SELECT ap_group_name FROM access_point_groups WHERE ap_group_id = '{}'".format(apGroupId))
        apGroupInfo = apGroupInfoCursor.fetchall()
        apGroupInfoCursor.close()
        for info in apGroupInfo:
            apGroupName = info[0]
        session['apGroupId'] = apGroupId
        session['apGroupName'] = apGroupName
        return render_template("manage-ap-group-dashboard.html")
    else:
        return redirect(url_for('index'))

@Cardinal.route("/config-ap-ip", methods=["GET"])
def configApIp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-ip.html", status=status)

@Cardinal.route("/do-config-ap-ip", methods=["POST"])
def doConfigApIp():
    if request.method == 'POST':
        apId = session.get('apId', None)
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
            apSshPassword = info[3]
        subprocess.check_output("scout --change-ip {0} {1} {2} {3} {4}".format(apIp,apSshUsername,apSshPassword,apNewIp,apSubnetMask), shell=True)
        status = "{}'s IP was successfully updated!".format(apName)
        sqlChangeApIpCursor = conn.cursor()
        sqlChangeApIpCursor.execute("UPDATE access_points SET ap_ip = '{0}' WHERE ap_id = '{1}'".format(apNewIp,apId))
        sqlChangeApIpCursor.close()
        conn.close()
        return redirect(url_for('configApIp', status=status))

@Cardinal.route("/config-ap-name", methods=["GET"])
def configApName():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-name.html", status=status)

@Cardinal.route("/do-config-ap-name", methods=["POST"])
def doConfigApName():
    if request.method == 'POST':
        apId = session.get('apId', None)
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
            apSshPassword = info[3]
        subprocess.check_output("scout --change-name {0} {1} {2} {3}".format(apIp,apSshUsername,apSshPassword,apNewName), shell=True)
        status = "AP Name Changed from {0} to {1}".format(apName,apNewName)
        sqlChangeApNameCursor = conn.cursor()
        sqlChangeApNameCursor.execute("UPDATE access_points SET ap_name = '{0}' WHERE ap_id = '{1}'".format(apName,apId))
        sqlChangeApNameCursor.close()
        conn.close()
        return redirect(url_for('configApName', status=status))

@Cardinal.route("/manage-ap-tftp-backup", methods=["GET"])
def manageApTftpBackup():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("manage-ap-tftp-backup.html", status=status)

@Cardinal.route("/manage-ap-tftp-group-backup", methods=["GET"])
def manageApTftpGroupBackup():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("manage-ap-tftp-group-backup.html", status=status)

@Cardinal.route("/do-ap-tftp-backup", methods=["POST"])
def doApTftpBackup():
    if request.method == 'POST':
        apId = session.get('apId', None)
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
            apSshPassword = info[3]
        subprocess.check_output("scout --tftp-backup {0} {1} {2} {3}".format(apIp,apSshUsername,apSshPassword,tftpIp), shell=True)
        status = "TFTP Config Backup for {} Successfully Initiated!".format(apName)
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
                apSshPassword = info[3]
                subprocess.check_output("scout --tftp-backup {0} {1} {2} {3}".format(apIp,apSshUsername,apSshPassword,tftpIp), shell=True)
            status = "TFTP Config Backup for {} Successfully Initiated!".format(apGroupName)
            conn.close()
            return redirect(url_for('manageApTftpBackupGroup', status=status))
        return redirect(url_for('manageApTftpBackup', status=status))

@Cardinal.route("/config-ap-http", methods=["GET"])
def configApHttp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-http.html", status=status)

@Cardinal.route("/do-enable-ap-http", methods=["POST"])
def doEnableApHttp():
    if request.method == 'POST':
        apId = session.get('apId', None)
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            apSshPassword = info[3]
        subprocess.check_output("scout --enable-http {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "HTTP Server for {} Successfully Enabled".format(apName)
        conn.close()
        return redirect(url_for('configApHttp', status=status))

@Cardinal.route("/do-disable-ap-http", methods=["POST"])
def doDisableApHttp():
    if request.method == 'POST':
        apId = session.get('apId', None)
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            apSshPassword = info[3]
        subprocess.check_output("scout --disable-http {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "HTTP Server for {} Successfully Disabled".format(apName)
        conn.close()
        return redirect(url_for('configApHttp', status=status))

@Cardinal.route("/config-ap-radius", methods=["GET"])
def configApRadius():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-radius.html", status=status)

@Cardinal.route("/do-enable-ap-radius", methods=["POST"])
def doEnableApRadius():
    if request.method == 'POST':
        apId = session.get('apId', None)
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            apSshPassword = info[3]
        subprocess.check_output("scout --enable-radius {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "RADIUS for {} Successfully Enabled".format(apName)
        conn.close()
        return redirect(url_for('configApRadius', status=status))

@Cardinal.route("/do-disable-ap-http", methods=["POST"])
def doDisableApRadius():
    if request.method == 'POST':
        apId = session.get('apId', None)
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            apSshPassword = info[3]
        subprocess.check_output("scout --disable-radius {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "RADIUS Server for {} Successfully Disabled".format(apName)
        conn.close()
        return redirect(url_for('configApRadius', status=status))

@Cardinal.route("/config-ap-snmp", methods=["GET"])
def configApSnmp():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("config-ap-snmp.html", status=status)

@Cardinal.route("/do-enable-ap-snmp", methods=["POST"])
def doEnableApSnmp():
    if request.method == 'POST':
        apId = session.get('apId', None)
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            apSshPassword = info[3]
        subprocess.check_output("scout --enable-snmp {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "SNMP for {} Successfully Enabled".format(apName)
        conn.close()
        return redirect(url_for('configApSnmp', status=status))

@Cardinal.route("/do-disable-ap-snmp", methods=["POST"])
def doDisableApSnmp():
    if request.method == 'POST':
        apId = session.get('apId', None)
        conn = cardinalSql()
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("SELECT ap_name,ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '{}'".format(apId))
        apInfo = apInfoCursor.fetchall()
        apInfoCursor.close()
        for info in apInfo:
            apName = info[0]
            apIp = info[1]
            apSshUsername = info[2]
            apSshPassword = info[3]
        subprocess.check_output("scout --disable-snmp {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "SNMP Server for {} Successfully Disabled".format(apName)
        conn.close()
        return redirect(url_for('configApSnmp', status=status))

@Cardinal.route("/add-ssids", methods=["GET"])
def addSsids():
    if session.get("username") is not None:
        return render_template("add-ssids.html")

@Cardinal.route("/add-ssid-24ghz", methods=["GET"])
def addSsid24Ghz():
    if session.get("username") is not None:
        return render_template("add-ssid-24ghz.html")

@Cardinal.route("/add-ssid-5ghz", methods=["GET"])
def addSsid5Ghz():
    if session.get("username") is not None:
        return render_template("add-ssid-5ghz.html")

@Cardinal.route("/add-ssid-24ghz-radius", methods=["GET"])
def addSsid24GhzRadius():
    if session.get("username") is not None:
        return render_template("add-ssid-24ghz-radius.html")

@Cardinal.route("/add-ssid-5ghz-radius", methods=["GET"])
def addSsid5GhzRadius():
    if session.get("username") is not None:
        return render_template("add-ssid-5ghz-radius.html")

@Cardinal.route("/delete-ssids", methods=["GET"])
def deleteSsids():
    if session.get("username") is not None:
        return render_template("delete-ssids.html")

@Cardinal.route("/total-ap-clients", methods=["GET"])
def totalApClients():
    if session.get("username") is not None:
        return render_template("total-ap-clients.html")

@Cardinal.route("/total-ap-bandwidth", methods=["GET"])
def totalApBandwidth():
    if session.get("username") is not None:
        return render_template("total-ap-bandwidth.html")

@Cardinal.route("/total-aps", methods=["GET"])
def totalAps():
    if session.get("username") is not None:
        conn = cardinalSql()
        totalApsCursor = conn.cursor()
        totalApsCursor.execute("SELECT COUNT(*) FROM access_points")
        totalAps = totalApsCursor.fetchone()[0]
        totalApsCursor.close()
        conn.close()
        return render_template('total-aps.html', totalAps=totalAps)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/total-clients", methods=["GET"])
def totalClients():
    if session.get("username") is not None:
        conn = cardinalSql()
        totalClientsCursor = conn.cursor()
        totalClientsCursor.execute("SELECT FORMAT(SUM(ap_total_clients),0) AS totalClients FROM access_points")
        totalClients = totalClientsCursor.fetchone()[0]
        totalClientsCursor.close()
        conn.close()
        return render_template('total-clients.html', totalClients=totalClients)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/total-ap-groups", methods=["GET"])
def totalApGroups():
    if session.get("username") is not None:
        conn = cardinalSql()
        totalApGroupsCursor = conn.cursor()
        totalApGroupsCursor.execute("SELECT COUNT(*) FROM access_point_groups")
        totalApGroups = totalApGroupsCursor.fetchone()[0]
        totalApGroupsCursor.close()
        conn.close()
        return render_template('total-ap-groups.html', totalApGroups=totalApGroups)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/total-ssids", methods=["GET"])
def totalSsids():
    if session.get("username") is not None:
        conn = cardinalSql()
        ssids24Cursor = conn.cursor()
        ssids5Cursor = conn.cursor()
        ssids24RadiusCursor = conn.cursor()
        ssids5RadiusCursor = conn.cursor()
        ssids24Cursor.execute("SELECT COUNT(*) FROM ssids_24ghz")
        ssids5Cursor.execute("SELECT COUNT(*) FROM ssids_5ghz")
        ssids24RadiusCursor.execute("SELECT COUNT(*) FROM ssids_24ghz_radius")
        ssids5RadiusCursor.execute("SELECT COUNT(*) FROM ssids_5ghz_radius")
        ssids24 = ssids24Cursor.fetchone()[0]
        ssids5 = ssids5Cursor.fetchone()[0]
        ssids24Radius = ssids24RadiusCursor.fetchone()[0]
        ssids5Radius = ssids5RadiusCursor.fetchone()[0]
        totalSsids = ssids24 + ssids5 + ssids24Radius + ssids5Radius
        ssids24Cursor.close()
        ssids5Cursor.close()
        ssids24RadiusCursor.close()
        ssids5RadiusCursor.close()
        conn.close()
        return render_template('total-ssids.html', totalSsids=totalSsids)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    Cardinal.run(debug=True, host='0.0.0.0')
