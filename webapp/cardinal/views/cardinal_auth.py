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
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash

cardinal_auth = Blueprint('cardinal_auth_bp', __name__)

@cardinal_auth.route("/")
def index():
    if session.get("username") is not None:
        return redirect(url_for('cardinal_auth_bp.dashboard'))
    else:
        return render_template("index.html")

@cardinal_auth.route("/dashboard")
def dashboard():
    if session.get("username") is not None:
        return render_template("dashboard.html")
    else:
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_auth.route("/login", methods=['POST'])
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
        return redirect(url_for('cardinal_auth_bp.dashboard'))
    elif dbUsername is None:
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'
    else:
        return 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'

@cardinal_auth.route("/logout")
def logout():
   session.pop('username', None)
   session.pop('apId', None)
   session.pop('apGroupId', None)
   session.pop('apGroupName', None)
   session.pop('apName', None)
   session.pop('apIp', None)
   session.pop('apTotalClients', None)
   session.pop('apBandwidth', None)
   return redirect(url_for('cardinal_auth_bp.index'))
