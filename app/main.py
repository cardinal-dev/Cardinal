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
    conn.close()
    if check_password_hash(hash,password):
        session['username'] = username
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
        apGroupCursor = conn.cursor()
        apGroupCursor.execute("SELECT ap_group_id,ap_group_name FROM access_point_groups")
        return render_template("add-ap.html")
    else:
        return redirect(url_for('index'))

@Cardinal.route("/submit-add-ap", methods=["POST"])
def submitAddAp():
    apName = request.form["ap_name"]
    apIp = request.form["ap_ip"]
    apSshUsername = request.form["ssh_username"]
    apSshPassword = request.form["ssh_password"]
    apGroupId = request.form["group_id"]
    apSnmp = request.form["ap_snmp"]
    status = "Success! {} was successfully registered!".format(apName)
    addApCursor = conn.cursor()
    addApCursor.execute("INSERT INTO access_points (ap_name, ap_ip, ap_ssh_username, ap_ssh_password, ap_snmp, ap_group_id) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(apName, apIp, apSshUsername, apSshPassword, ap_snmp, ap_group_id))
    conn.commit()
    return render_template('add-ap.html', status=status)

@Cardinal.route("/add-ap-group", methods=["GET"])
def addApGroup():
    if session.get("username") is not None:
        return render_template("add-ap-group.html")
    else:
        return redirect(url_for('index'))

@Cardinal.route("/submit-add-ap-group", methods=["POST"])
def submitAddApGroup():
    apGroupName = request.form["ap_group_name"]
    status = "Success! {} was successfully registered!".format(apGroupName)
    addApGroupCursor = conn.cursor()
    addApGroupCursor.execute("INSERT INTO access_point_groups (ap_group_name) VALUES ('{}')".format(apGroupName))
    conn.commit()
    return render_template('add-ap-group.html', status=status)

if __name__ == "__main__":
    Cardinal.run(debug=True, host='0.0.0.0')
