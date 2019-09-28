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

# FLASK APP INITIALIZATION

Cardinal = Flask(__name__)

# SYSTEM VARIABLES

cardinalConfigFile = os.environ['CARDINALCONFIG']
cardinalConfig = ConfigParser()
cardinalConfig.read("{}".format(cardinalConfigFile))
cardinalLogFile = cardinalConfig.get('cardinal', 'logfile')
logging.basicConfig(filename='{}'.format(cardinalLogFile), filemode='w', format='%(name)s - %(levelname)s - %(message)s')
cardinalSecretKey = cardinalConfig.get('cardinal', 'secretkey')
Cardinal.secret_key = "{}".format(cardinalSecretKey)

# MySQL AUTHENTICATION & HANDLING

mysqlHost = cardinalConfig.get('cardinal', 'dbserver')
mysqlUser = cardinalConfig.get('cardinal', 'dbuser')
mysqlPass = cardinalConfig.get('cardinal', 'dbpassword')
mysqlDb = cardinalConfig.get('cardinal', 'dbname')

def cardinalSql():
    conn = MySQLdb.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPass, db = mysqlDb)
    return conn

# CARDINAL FLASK ROUTES

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
        logging.warning("Unauthorized access detected. Someone tried logging into Cardinal but was unsuccessful.")
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'
    if check_password_hash(dbHash,password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    elif dbUsername is None:
        logging.warning("Unauthorized access detected. Someone tried logging into Cardinal but was unsuccessful.")
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'
    else:
        logging.warning("Unauthorized access detected. Someone tried logging into Cardinal but was unsuccessful.")
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

@Cardinal.route("/do-add-ap", methods=["POST"])
def doAddAp():
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

@Cardinal.route("/do-delete-ap", methods=["POST"])
def doDeleteAp():
    if request.method == 'POST':
        apId = request.form["ap_id"]
        conn = cardinalSql()
        deleteApNameCursor = conn.cursor()
        deleteApNameCursor.execute("SELECT ap_name FROM access_points WHERE ap_id = '{}'".format(apId))
        apName = deleteApNameCursor.fetchone()[0]
        deleteApNameCursor.close()
        status = "Success! {} was successfully registered!".format(apName)
        try:
            deleteApCursor = conn.cursor()
            deleteApCursor.execute("DELETE FROM access_points WHERE ap_id = '{}'".format(apId))
            deleteApCursor.close()
        except MySQLdb.Error as e:
            status = e
        finally:
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

@Cardinal.route("/do-add-ap-group", methods=["POST"])
def doAddApGroup():
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

@Cardinal.route("/do-delete-ap-group", methods=["POST"])
def doDeleteApGroup():
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
            apSshPassword = info[3]
        subprocess.check_output("scout --enable-http {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "HTTP Server for {} Successfully Enabled".format(apName)
        conn.close()
        return redirect(url_for('configApHttp', status=status))

@Cardinal.route("/do-disable-ap-http", methods=["POST"])
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
            apSshPassword = info[3]
        subprocess.check_output("scout --enable-radius {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "RADIUS for {} Successfully Enabled".format(apName)
        conn.close()
        return redirect(url_for('configApRadius', status=status))

@Cardinal.route("/do-disable-ap-http", methods=["POST"])
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
            apSshPassword = info[3]
        subprocess.check_output("scout --enable-snmp {0} {1} {2}".format(apIp,apSshUsername,apSshPassword), shell=True)
        status = "SNMP for {} Successfully Enabled".format(apName)
        conn.close()
        return redirect(url_for('configApSnmp', status=status))

@Cardinal.route("/do-disable-ap-snmp", methods=["POST"])
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
        status = request.args.get('status')
        return render_template("add-ssid-24ghz.html", status=status)

@Cardinal.route("/do-add-ssid-24ghz", methods=["POST"])
def doAddSsid24Ghz():
    if request.method == 'POST':
        ssidName = request.form["ssid_name"]
        vlan = request.form["vlan"]
        wpa2Psk = request.form["wpa2_psk"]
        bridgeGroup = request.form["bridge_group_id"]
        radioId = request.form["radio_sub_id"]
        gigaId = request.form["giga_sub_id"]
        conn = cardinalSql()
        addSsid24GhzCursor = conn.cursor()
        addSsid24GhzCursor.execute("INSERT INTO ssids_24ghz (ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(ssidName,vlan,wpa2Psk,bridgeGroup,radioId,gigaId))
        addSsid24GhzCursor.close()
        conn.commit()
        conn.close()
        status = "Success! {} was successfully registered!".format(ssidName)
        return redirect(url_for('addSsid24Ghz', status=status))

@Cardinal.route("/add-ssid-5ghz", methods=["GET"])
def addSsid5Ghz():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("add-ssid-5ghz.html", status=status)

@Cardinal.route("/do-add-ssid-5ghz", methods=["POST"])
def doAddSsid5Ghz():
    if request.method == 'POST':
        ssidName = request.form["ssid_name"]
        vlan = request.form["vlan"]
        wpa2Psk = request.form["wpa2_psk"]
        bridgeGroup = request.form["bridge_group_id"]
        radioId = request.form["radio_sub_id"]
        gigaId = request.form["giga_sub_id"]
        conn = cardinalSql()
        addSsid5GhzCursor = conn.cursor()
        addSsid5GhzCursor.execute("INSERT INTO ssids_5ghz (ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(ssidName,vlan,wpa2Psk,bridgeGroup,radioId,gigaId))
        addSsid5GhzCursor.close()
        conn.commit()
        conn.close()
        status = "Success! {} was successfully registered!".format(ssidName)
        return redirect(url_for('addSsid5Ghz', status=status))

@Cardinal.route("/add-ssid-24ghz-radius", methods=["GET"])
def addSsid24GhzRadius():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("add-ssid-24ghz-radius.html", status=status)

@Cardinal.route("/do-add-ssid-24ghz-radius", methods=["POST"])
def doAddSsid24GhzRadius():
    if request.method == 'POST':
        ssidName = request.form["ssid_name"]
        vlan = request.form["vlan"]
        bridgeGroup = request.form["bridge_group_id"]
        radioId = request.form["radio_sub_id"]
        gigaId = request.form["giga_sub_id"]
        radiusIp = request.form["radius_ip"]
        sharedSecret = request.form["shared_secret"]
        authPort = request.form["auth_port"]
        acctPort = request.form["acct_port"]
        radiusTimeout = request.form["radius_timeout"]
        radiusGroup = request.form["radius_group"]
        methodList = request.form["method_list"]
        conn = cardinalSql()
        addSsid24GhzRadiusCursor = conn.cursor()
        addSsid24GhzRadiusCursor.execute("INSERT INTO ssids_24ghz_radius (ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')".format(ssidName,vlan,bridgeGroup,radioId,gigaId,radiusIp,sharedSecret,authPort,acctPort,radiusTimeout,radiusGroup,methodList))
        addSsid24GhzRadiusCursor.close()
        conn.commit()
        conn.close()
        status = "Success! {} was successfully registered!".format(ssidName)
        return redirect(url_for('addSsid24GhzRadius', status=status))

@Cardinal.route("/add-ssid-5ghz-radius", methods=["GET"])
def addSsid5GhzRadius():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("add-ssid-5ghz-radius.html", status=status)

@Cardinal.route("/do-add-ssid-5ghz-radius", methods=["POST"])
def doAddSsid5GhzRadius():
    if request.method == 'POST':
        ssidName = request.form["ssid_name"]
        vlan = request.form["vlan"]
        bridgeGroup = request.form["bridge_group_id"]
        radioId = request.form["radio_sub_id"]
        gigaId = request.form["giga_sub_id"]
        radiusIp = request.form["radius_ip"]
        sharedSecret = request.form["shared_secret"]
        authPort = request.form["auth_port"]
        acctPort = request.form["acct_port"]
        radiusTimeout = request.form["radius_timeout"]
        radiusGroup = request.form["radius_group"]
        methodList = request.form["method_list"]
        conn = cardinalSql()
        addSsid5GhzRadiusCursor = conn.cursor()
        addSsid5GhzRadiusCursor.execute("INSERT INTO ssids_5ghz_radius (ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')".format(ssidName,vlan,bridgeGroup,radioId,gigaId,radiusIp,sharedSecret,authPort,acctPort,radiusTimeout,radiusGroup,methodList))
        addSsid5GhzRadiusCursor.close()
        conn.commit()
        conn.close()
        status = "Success! {} was successfully registered!".format(ssidName)
        return redirect(url_for('addSsid5GhzRadius', status=status))

@Cardinal.route("/deploy-ssids", methods=["GET"])
def deploySsids():
    if session.get("username") is not None:
        return render_template("deploy-ssids.html")

@Cardinal.route("/deploy-ssids-group", methods=["GET"])
def deploySsidsGroup():
    if session.get("username") is not None:
        return render_template("deploy-ssids-group.html")

@Cardinal.route("/deploy-ssid-24ghz", methods=["GET"])
def deploySsid24Ghz():
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
        return redirect(url_for('index'))

@Cardinal.route("/deploy-ssid-24ghz-group", methods=["GET"])
def deploySsid24GhzGroup():
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

@Cardinal.route("/do-deploy-ssid-24ghz", methods=["POST"])
def doDeploySsid24Ghz():
    conn = cardinalSql()
    ssidId = request.form["ssid_id"]
    apId = session.get('apId')
    apName = session.get('apName')
    conn = cardinalSql()
    try:
        checkSsidRelationship = conn.cursor()
        checkSsidRelationship.execute("INSERT INTO ssids_24ghz_deployed (ap_id,ssid_id) VALUES ('{}', '{}')".format(apId,ssidId))
        checkSsidRelationship.close()
    except MySQLdb.Error as e:
        status = "{0} already has the SSID deployed: {1}".format(apName,e)
        logging.error("{0} already has the SSID deployed: {1}".format(apName,e))
        return redirect(url_for('deploySsid24Ghz', status=status))
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
            apSshPassword = info[3]
        subprocess.check_output("scout --create-ssid-24 {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(apIp,apSshUsername,apSshPassword,ssid,wpa2Pass,vlan,bridgeGroup,radioSub,gigaSub), shell=True)
        status = "The Deployment of 2.4GHz SSID {0} for AP {1} Has Been Successfully Initiated!".format(ssid,apName)
    finally:
        conn.commit()
        conn.close()
        return redirect(url_for('deploySsid24Ghz', status=status))

@Cardinal.route("/do-deploy-ssid-24ghz-group", methods=["POST"])
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
            status = "{0} already has the SSID deployed: {1}".format(apName,e)
            logging.error("{0} already has the SSID deployed: {1}".format(apName,e))
            return redirect(url_for('deploySsid24GhzGroup', status=status))
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
                apSshPassword = info[2]
            subprocess.check_output("scout --create-ssid-24 {0} {1} {2} {3} {4} {5} {6} {7} {8}".format(apIp,apSshUsername,apSshPassword,ssid,wpa2Pass,vlan,bridgeGroup,radioSub,gigaSub), shell=True)
            status = "The Deployment of 2.4GHz SSID {0} for AP Group {1} Has Been Successfully Initiated!".format(ssid,apGroupName)
            conn.commit()
    conn.close()
    return redirect(url_for('deploySsid24GhzGroup', status=status))

@Cardinal.route("/delete-ssids", methods=["GET"])
def deleteSsids():
    if session.get("username") is not None:
        return render_template("delete-ssids.html")

@Cardinal.route("/delete-ssid-24ghz", methods=["GET"])
def deleteSsid24Ghz():
    if session.get("username") is not None:
        conn = cardinalSql()
        status = request.args.get('status')
        deleteSsidCursor = conn.cursor()
        deleteSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz")
        ssids = deleteSsidCursor.fetchall()
        deleteSsidCursor.close()
        conn.close()
        return render_template("delete-ssid-24ghz.html", status=status, ssids=ssids)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/do-delete-ssid-24ghz", methods=["POST"])
def doDeleteSsid24Ghz():
    if request.method == 'POST':
        ssidId = request.form["ssid_id"]
        conn = cardinalSql()
        deleteSsidNameCursor = conn.cursor()
        deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_24ghz WHERE ap_ssid_id = '{}'".format(ssidId))
        ssidName = deleteSsidNameCursor.fetchone()[0]
        deleteSsidNameCursor.close()
        status = "Success! {} was successfully deleted!".format(ssidName)
        try:
            deleteSsidCursor = conn.cursor()
            deleteSsidCursor.execute("DELETE FROM ssids_24ghz WHERE ap_ssid_id = '{}'".format(ssidId))
            deleteSsidCursor.close()
        except MySQLdb.Error as e:
            status = e
        finally:
            conn.commit()
            conn.close()
            return redirect(url_for('deleteSsid24Ghz', status=status))

@Cardinal.route("/delete-ssid-5ghz", methods=["GET"])
def deleteSsid5Ghz():
    if session.get("username") is not None:
        conn = cardinalSql()
        status = request.args.get('status')
        deleteSsidCursor = conn.cursor()
        deleteSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz")
        ssids = deleteSsidCursor.fetchall()
        deleteSsidCursor.close()
        conn.close()
        return render_template("delete-ssid-5ghz.html", status=status, ssids=ssids)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/do-delete-ssid-5ghz", methods=["POST"])
def doDeleteSsid5Ghz():
    if request.method == 'POST':
        ssidId = request.form["ssid_id"]
        conn = cardinalSql()
        deleteSsidNameCursor = conn.cursor()
        deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_5ghz WHERE ap_ssid_id = '{}'".format(ssidId))
        ssidName = deleteSsidNameCursor.fetchone()[0]
        deleteSsidNameCursor.close()
        status = "Success! {} was successfully deleted!".format(ssidName)
        deleteSsidCursor = conn.cursor()
        deleteSsidCursor.execute("DELETE FROM ssids_5ghz WHERE ap_ssid_id = '{}'".format(ssidId))
        deleteSsidCursor.close()
        conn.commit()
        conn.close()
        return redirect(url_for('deleteSsid5Ghz', status=status))

@Cardinal.route("/delete-ssid-24ghz-radius", methods=["GET"])
def deleteSsid24GhzRadius():
    if session.get("username") is not None:
        conn = cardinalSql()
        status = request.args.get('status')
        deleteSsidCursor = conn.cursor()
        deleteSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_24ghz_radius")
        ssids = deleteSsidCursor.fetchall()
        deleteSsidCursor.close()
        conn.close()
        return render_template("delete-ssid-24ghz-radius.html", status=status, ssids=ssids)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/do-delete-ssid-24ghz-radius", methods=["POST"])
def doDeleteSsid24GhzRadius():
    if request.method == 'POST':
        ssidId = request.form["ssid_id"]
        conn = cardinalSql()
        deleteSsidNameCursor = conn.cursor()
        deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_24ghz_radius WHERE ap_ssid_id = '{}'".format(ssidId))
        ssidName = deleteSsidNameCursor.fetchone()[0]
        deleteSsidNameCursor.close()
        status = "Success! {} was successfully deleted!".format(ssidName)
        deleteSsidCursor = conn.cursor()
        deleteSsidCursor.execute("DELETE FROM ssids_24ghz_radius WHERE ap_ssid_id = '{}'".format(ssidId))
        deleteSsidCursor.close()
        conn.commit()
        conn.close()
        return redirect(url_for('deleteSsid24GhzRadius', status=status))

@Cardinal.route("/delete-ssid-5ghz-radius", methods=["GET"])
def deleteSsid5GhzRadius():
    if session.get("username") is not None:
        conn = cardinalSql()
        status = request.args.get('status')
        deleteSsidCursor = conn.cursor()
        deleteSsidCursor.execute("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz_radius")
        ssids = deleteSsidCursor.fetchall()
        deleteSsidCursor.close()
        conn.close()
        return render_template("delete-ssid-5ghz-radius.html", status=status, ssids=ssids)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/do-delete-ssid-5ghz-radius", methods=["POST"])
def doDeleteSsid5GhzRadius():
    if request.method == 'POST':
        ssidId = request.form["ssid_id"]
        conn = cardinalSql()
        deleteSsidNameCursor = conn.cursor()
        deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_5ghz_radius WHERE ap_ssid_id = '{}'".format(ssidId))
        ssidName = deleteSsidNameCursor.fetchone()[0]
        deleteSsidNameCursor.close()
        status = "Success! {} was successfully deleted!".format(ssidName)
        deleteSsidCursor = conn.cursor()
        deleteSsidCursor.execute("DELETE FROM ssids_5ghz_radius WHERE ap_ssid_id = '{}'".format(ssidId))
        deleteSsidCursor.close()
        conn.commit()
        conn.close()
        return redirect(url_for('deleteSsid5GhzRadius', status=status))

@Cardinal.route("/total-ap-clients", methods=["GET"])
def totalApClients():
    if session.get("username") is not None:
        return render_template("total-ap-clients.html")

@Cardinal.route("/total-ap-bandwidth", methods=["GET"])
def totalApBandwidth():
    if session.get("username") is not None:
        return render_template("total-ap-bandwidth.html")

@Cardinal.route("/ap-ip-address", methods=["GET"])
def apIpAddress():
    if session.get("username") is not None:
        return render_template("ap-ip-address.html")

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

@Cardinal.route("/total-ap-group-clients", methods=["GET"])
def totalApGroupClients():
    if session.get("username") is not None:
        apGroupId = session.get("apGroupId")
        conn = cardinalSql()
        totalApGroupClientsCursor = conn.cursor()
        totalApGroupClientsCursor.execute("SELECT FORMAT(SUM(ap_total_clients),0) FROM access_points WHERE ap_group_id = '{}'".format(apGroupId))
        totalApGroupClients = totalApGroupClientsCursor.fetchone()[0]
        totalApGroupClientsCursor.close()
        conn.close()
        return render_template('total-ap-group-clients.html', totalApGroupClients=totalApGroupClients)
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
    Cardinal.run(host='0.0.0.0')
