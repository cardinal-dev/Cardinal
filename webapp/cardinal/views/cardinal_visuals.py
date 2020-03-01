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
from flask import redirect
from flask import session
from flask import url_for

cardinal_visuals = Blueprint('cardinal_visuals_bp', __name__)

@cardinal_visuals.route("/total-ap-clients", methods=["GET"])
def totalApClients():
    if session.get("username") is not None:
        return render_template("total-ap-clients.html")

@cardinal_visuals.route("/total-ap-bandwidth", methods=["GET"])
def totalApBandwidth():
    if session.get("username") is not None:
        return render_template("total-ap-bandwidth.html")

@cardinal_visuals.route("/ap-ip-address", methods=["GET"])
def apIpAddress():
    if session.get("username") is not None:
        return render_template("ap-ip-address.html")

@cardinal_visuals.route("/ap-model", methods=["GET"])
def apModel():
    if session.get("username") is not None:
        return render_template("ap-model.html")

@cardinal_visuals.route("/total-aps", methods=["GET"])
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
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_visuals.route("/total-clients", methods=["GET"])
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
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_visuals.route("/total-ap-groups", methods=["GET"])
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
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_visuals.route("/total-ap-group-clients", methods=["GET"])
def totalApGroupClients():
    if session.get("username") is not None:
        apGroupId = session.get("apGroupId")
        conn = cardinalSql()
        totalApGroupClientsCursor = conn.cursor()
        totalApGroupClientsCursor.execute("SELECT FORMAT(SUM(ap_total_clients),0) FROM access_points WHERE ap_group_id = %s", [apGroupId])
        totalApGroupClients = totalApGroupClientsCursor.fetchone()[0]
        totalApGroupClientsCursor.close()
        conn.close()
        return render_template('total-ap-group-clients.html', totalApGroupClients=totalApGroupClients)
    else:
        return redirect(url_for('cardinal_auth_bp.index'))

@cardinal_visuals.route("/total-ssids", methods=["GET"])
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
        return redirect(url_for('cardinal_auth_bp.index'))
