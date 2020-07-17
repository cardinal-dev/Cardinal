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
from cardinal.system.cardinal_sys import msgResourceAdded
from cardinal.system.cardinal_sys import msgSpecifyValidApGroup
from cardinal.system.cardinal_sys import msgResourceDeleted
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_ap_group = Blueprint('cardinal_ap_group_bp', __name__)

@cardinal_ap_group.route("/add-ap-group", methods=["GET", "POST"])
def addApGroup():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("add-ap-group.html", status=status)
        else:
            return redirect(url_for('cardinal_auth_bp.index'))
    elif request.method == 'POST':
        if session.get('username') is not None:
            apGroupName = request.form["ap_group_name"]
            status = msgResourceAdded(resource=apGroupName)
            conn = cardinalSql()
            try:
                addApGroupCursor = conn.cursor()
                addApGroupCursor.execute("INSERT INTO access_point_groups (ap_group_name) VALUES (%s)", [apGroupName])
                addApGroupCursor.close()
            except MySQLdb.Error as e:
                return redirect(url_for('cardinal_ap_group_bp.addApGroup', status=e))
            else:
                conn.commit()
            conn.close()
            return render_template('add-ap-group.html', status=status)
        else:
            return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_ap_group.route("/delete-ap-group", methods=["GET", "POST"])
def deleteApGroup():
    if request.method == 'GET':
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
    elif request.method == 'POST':
        if session.get("username") is not None:
            apGroupId = request.form["ap_group_id"]
            if len(apGroupId) <= 0:
                status = msgSpecifyValidApGroup()
                return redirect(url_for('cardinal_ap_group_bp.deleteApGroup', status=status))
            else:
                conn = cardinalSql()
                deleteApGroupNameCursor = conn.cursor()
                deleteApGroupNameCursor.execute("SELECT ap_group_name FROM access_point_groups WHERE ap_group_id = %s", [apGroupId])
                apGroupName = deleteApGroupNameCursor.fetchone()[0]
                status = msgResourceDeleted(resource=apGroupName)
                try:
                    deleteApGroupCursor = conn.cursor()
                    deleteApGroupCursor.execute("DELETE FROM access_point_groups WHERE ap_group_id = %s", [apGroupId])
                    deleteApGroupCursor.close()
                except MySQLdb.Error as e:
                    return redirect(url_for('cardinal_ap_group_bp.deleteApGroup', status=e))
                else:
                    conn.commit()
                    conn.close()
            return redirect(url_for('cardinal_ap_group_bp.deleteApGroup', status=status))

@cardinal_ap_group.route("/manage-ap-group-dashboard", methods=["GET", "POST"])
def chooseApGroupDashboard():
    if request.method == 'GET':
        if session.get("username") is not None:
            conn = cardinalSql()
            status = request.args.get('status')
            apGroupCursor = conn.cursor()
            apGroupCursor.execute("SELECT ap_group_id,ap_group_name FROM access_point_groups")
            apGroups = apGroupCursor.fetchall()
            apGroupCursor.close()
            conn.close()
            return render_template("choose-ap-group-dashboard.html", apGroups=apGroups, status=status)
        else:
            return redirect(url_for('cardinal_auth_bp.index'))
    elif request.method == 'POST':
        if session.get("username") is not None:
            apGroupId = request.form["ap_group_id"]
            if len(apGroupId) <= 0:
                status = msgSpecifyValidApGroup()
                return redirect(url_for('cardinal_ap_group_bp.chooseApGroupDashboard', status=status))
            else:
                conn = cardinalSql()
                apGroupNameCursor = conn.cursor()
                apGroupNameCursor.execute("SELECT ap_group_name FROM access_point_groups WHERE ap_group_id = %s", [apGroupId])
                apGroupName = apGroupNameCursor.fetchone()[0]
                apGroupNameCursor.close()
                session['apGroupId'] = apGroupId
                session['apGroupName'] = apGroupName
                conn.close()
                return render_template("manage-ap-group-dashboard.html")
        elif session.get("username") is None:
            return redirect(url_for('cardinal_auth_bp.index'))
