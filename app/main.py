#!/usr/bin/env python3

# Cardinal Flask Configuration
# Author: falcon78921

import mysql.connector
from configparser import ConfigParser
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response
from flask import session
from flask import url_for
from urllib.parse import urlparse
from werkzeug.security import check_password_hash

# Flask app intitialization

Cardinal = Flask(__name__)
Cardinal.secret_key = "SECRET_KEY_HERE"

# MySQL authentication

mysqlConfig = ConfigParser()
mysqlConfig.read("/home/cardinal/cardinal.ini")
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
        return redirect(url_for('dashboard'))
    else:
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'

@Cardinal.route("/logout")
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

if __name__ == "__main__":
    Cardinal.run(debug=True, host='0.0.0.0')
