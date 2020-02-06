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
from cardinal.system.cardinal_sys import MySQLdb
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_ap_group = Blueprint('cardinal_ap_group_bp', __name__)

@cardinal_ap_group.route("/add-ap-group", methods=["GET"])
def addApGroup():
    if session.get("username") is not None:
        status = request.args.get('status')
        return render_template("add-ap-group.html", status=status)
    else:
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_ap_group.route("/do-add-ap-group", methods=["POST"])
def doAddApGroup():
    if request.method == 'POST':
        apGroupName = request.form["ap_group_name"]
        status = "{} was successfully registered!".format(apGroupName)
        conn = cardinalSql()
        try:
            addApGroupCursor = conn.cursor()
            addApGroupCursor.execute("INSERT INTO access_point_groups (ap_group_name) VALUES ('{}')".format(apGroupName))
            addApGroupCursor.close()
        except MySQLdb.Error as e:
            return redirect(url_for('cardinal_ap_group_bp.addApGroup', status=e))
        else:
            conn.commit()
        conn.close()
        return render_template('add-ap-group.html', status=status)

@cardinal_ap_group.route("/delete-ap-group", methods=["GET"])
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
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_ap_group.route("/do-delete-ap-group", methods=["POST"])
def doDeleteApGroup():
    if request.method == 'POST':
        apGroupId = request.form["ap_group_id"]
        if len(apGroupId) <= 0:
            status = "Please select a valid access point group."
            return redirect(url_for('cardinal_ap_group_bp.deleteApGroup', status=status))
        conn = cardinalSql()
        deleteApGroupNameCursor = conn.cursor()
        deleteApGroupNameCursor.execute("SELECT ap_group_name FROM access_point_groups WHERE ap_group_id = '{}'".format(apGroupId))
        apGroupName = deleteApGroupNameCursor.fetchone()[0]
        status = "{} was successfully deleted!".format(apGroupName)
        try:
            deleteApGroupCursor = conn.cursor()
            deleteApGroupCursor.execute("DELETE FROM access_point_groups WHERE ap_group_id = '{}'".format(apGroupId))
            deleteApGroupCursor.close()
        except MySQLdb.Error as e:
            return redirect(url_for('cardinal_ap_group_bp.deleteApGroup', status=e))
        else:
            conn.commit()
        conn.close()
        return redirect(url_for('cardinal_ap_group_bp.deleteApGroup', status=status))

@cardinal_ap_group.route("/choose-ap-group-dashboard", methods=["GET"])
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
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_ap_group.route("/manage-ap-group-dashboard", methods=["POST"])
def manageApGroupDashboard():
    if request.method == 'POST':
        apId = session.get("apId", None)
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
        return redirect(url_for('cardinal_auth_bp.index'))
