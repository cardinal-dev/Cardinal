#!/usr/bin/env python3

# Cardinal Flask Configuration
# Author: falcon78921

import mysql.connector
from configparser import ConfigParser
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash

# Flask app intitialization

Cardinal = Flask(__name__)
Cardinal.secret_key = "SECRET_KEY_HERE"

# MySQL authentication

mysqlConfig = ConfigParser()
mysqlConfig.read("/path/to/cardinal.ini")
mysqlHost = mysqlConfig.get('cardinal_mysql_config', 'servername')
mysqlUser = mysqlConfig.get('cardinal_mysql_config', 'username')
mysqlPass = mysqlConfig.get('cardinal_mysql_config', 'password')
mysqlDb = mysqlConfig.get('cardinal_mysql_config', 'dbname')
conn = mysql.connector.connect(host = mysqlHost, user = mysqlUser, passwd = mysqlPass, db = mysqlDb)

# Flask routes

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
    loginCursor = conn.cursor()
    loginCursor.execute("SELECT password FROM users WHERE username = '{}'".format(username))
    hash = loginCursor.fetchone()[0]
    if check_password_hash(hash,password):
        session['username'] = username
        loginCursor.close()
        return redirect(url_for('dashboard'))
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
        apGroupCursor = conn.cursor()
        apGroupCursor.execute("SELECT ap_group_id,ap_group_name FROM access_point_groups")
        apGroups = apGroupCursor.fetchall()
        apGroupCursor.close()
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
        addApCursor = conn.cursor()
        addApCursor.execute("INSERT INTO access_points (ap_name, ap_ip, ap_ssh_username, ap_ssh_password, ap_snmp, ap_group_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(apName, apIp, apSshUsername, apSshPassword, apSnmp, apGroupId))
        conn.commit()
        addApCursor.close()
        return redirect(url_for('addAp', status=status))

@Cardinal.route("/delete-ap", methods=["GET"])
def deleteAp():
    if session.get("username") is not None:
        status = request.args.get('status')
        apCursor = conn.cursor()
        apCursor.execute("SELECT ap_id,ap_name FROM access_points")
        aps = apCursor.fetchall()
        apCursor.close()
        return render_template("delete-ap.html", aps=aps, status=status)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/submit-delete-ap", methods=["POST"])
def submitDeleteAp():
    if request.method == 'POST':
        apId = request.form["ap_id"]
        deleteApNameCursor = conn.cursor()
        deleteApNameCursor.execute("SELECT ap_name FROM access_points WHERE ap_id = '{}'".format(apId))
        apName = deleteApNameCursor.fetchone()[0]
        status = "Success! {} was successfully registered!".format(apName)
        deleteApCursor = conn.cursor()
        deleteApCursor.execute("DELETE FROM access_points WHERE ap_id = '{}'".format(apId))
        deleteApCursor.close()
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
        addApGroupCursor = conn.cursor()
        addApGroupCursor.execute("INSERT INTO access_point_groups (ap_group_name) VALUES ('{}')".format(apGroupName))
        addApGroupCursor.close()
        conn.commit()
        return render_template('add-ap-group.html', status=status)

@Cardinal.route("/delete-ap-group", methods=["GET"])
def deleteApGroup():
    if session.get("username") is not None:
        status = request.args.get('status')
        deleteApGroupCursor = conn.cursor()
        deleteApGroupCursor.execute("SELECT ap_group_id,ap_group_name FROM access_point_groups")
        apGroups = deleteApGroupCursor.fetchall()
        deleteApGroupCursor.close()
        return render_template("delete-ap-group.html", status=status, apGroups=apGroups)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/submit-delete-ap-group", methods=["POST"])
def submitDeleteApGroup():
    if request.method == 'POST':
        apGroupId = request.form["ap_group_id"]
        deleteApGroupNameCursor = conn.cursor()
        deleteApGroupNameCursor.execute("SELECT ap_group_name FROM access_point_groups WHERE ap_group_id = '{}'".format(apGroupId))
        apGroupName = deleteApGroupNameCursor.fetchone()[0]
        status = "Success! {} was successfully deleted!".format(apGroupName)
        deleteApGroupCursor = conn.cursor()
        deleteApGroupCursor.execute("DELETE FROM access_point_groups WHERE ap_group_id = '{}'".format(apGroupId))
        deleteApGroupCursor.close()
        return redirect(url_for('deleteApGroup', status=status))

@Cardinal.route("/network-tools", methods=["GET"])
def networkTools():
    if session.get("username") is not None:
        return render_template("network-tools.html")
    else:
        return redirect(url_for('index'))

@Cardinal.route("/total-aps", methods=["GET"])
def totalAps():
    if session.get("username") is not None:
        totalApsCursor = conn.cursor(buffered=True)
        totalApsCursor.execute("SELECT * FROM access_points")
        totalAps = totalApsCursor.rowcount
        totalApsCursor.close()
        return render_template('total-aps.html', totalAps=totalAps)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/total-clients", methods=["GET"])
def totalClients():
    if session.get("username") is not None:
        totalClientsCursor = conn.cursor(buffered=True)
        totalClientsCursor.execute("SELECT SUM(ap_total_clients) AS totalClients FROM access_points WHERE ap_all_id = 2")
        totalClients = totalClientsCursor.fetchone()[0]
        totalClientsCursor.close()
        return render_template('total-clients.html', totalClients=totalClients)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/total-ap-groups", methods=["GET"])
def totalApGroups():
    if session.get("username") is not None:
        totalApGroupsCursor = conn.cursor(buffered=True)
        totalApGroupsCursor.execute("SELECT COUNT(*) AS totalAPGroups FROM access_point_groups")
        totalApGroups = totalApGroupsCursor.fetchone()[0]
        totalApGroupsCursor.close()
        return render_template('total-ap-groups.html', totalApGroups=totalApGroups)
    else:
        return redirect(url_for('index'))

@Cardinal.route("/total-ssids", methods=["GET"])
def totalSsids():
    if session.get("username") is not None:
        ssids24Cursor = conn.cursor(buffered=True)
        ssids5Cursor = conn.cursor(buffered=True)
        ssids24RadiusCursor = conn.cursor(buffered=True)
        ssids5RadiusCursor = conn.cursor(buffered=True)
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
        return render_template('total-ssids.html', totalSsids=totalSsids)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    Cardinal.run(debug=True, host='0.0.0.0')
