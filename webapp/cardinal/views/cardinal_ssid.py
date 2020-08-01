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
from cardinal.system.cardinal_sys import msgAuthFailed
from cardinal.system.cardinal_sys import msgResourceAdded
from cardinal.system.cardinal_sys import msgResourceDeleted
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_ssid = Blueprint('cardinal_ssid_bp', __name__)

@cardinal_ssid.route("/add-ssids", methods=["GET"])
def addSsids():
    if session.get("username") is not None:
        return render_template("add-ssids.html")
    elif session.get("username") is None:
        return msgAuthFailed, 401

@cardinal_ssid.route("/add-ssid-24ghz", methods=["GET", "POST"])
def addSsid24Ghz():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("add-ssid-24ghz.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidName = request.form["ssid_name"]
            vlan = request.form["vlan"]
            wpa2Psk = bytes(request.form["wpa2_psk"], 'utf-8')
            bridgeGroup = request.form["bridge_group_id"]
            radioId = request.form["radio_sub_id"]
            gigaId = request.form["giga_sub_id"]
            encryptedWpa2 = cipherSuite.encrypt(wpa2Psk).decode('utf-8')
            conn = cardinalSql()
            addSsid24GhzCursor = conn.cursor()
            addSsid24GhzCursor.execute("INSERT INTO ssids_24ghz (ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id) VALUES (%s, %s, %s, %s, %s, %s)", (ssidName,vlan,encryptedWpa2,bridgeGroup,radioId,gigaId))
            addSsid24GhzCursor.close()
            conn.commit()
            conn.close()
            status = msgResourceAdded(resource=ssidName)
            return redirect(url_for('cardinal_ssid_bp.addSsid24Ghz', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/add-ssid-5ghz", methods=["GET", "POST"])
def addSsid5Ghz():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("add-ssid-5ghz.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidName = request.form["ssid_name"]
            vlan = request.form["vlan"]
            wpa2Psk = bytes(request.form["wpa2_psk"], 'utf-8')
            bridgeGroup = request.form["bridge_group_id"]
            radioId = request.form["radio_sub_id"]
            gigaId = request.form["giga_sub_id"]
            encryptedWpa2 = cipherSuite.encrypt(wpa2Psk).decode('utf-8')
            conn = cardinalSql()
            addSsid5GhzCursor = conn.cursor()
            addSsid5GhzCursor.execute("INSERT INTO ssids_5ghz (ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id) VALUES (%s, %s, %s, %s, %s, %s)", (ssidName,vlan,encryptedWpa2,bridgeGroup,radioId,gigaId))
            addSsid5GhzCursor.close()
            conn.commit()
            conn.close()
            status = msgResourceAdded(resource=ssidName)
            return redirect(url_for('cardinal_ssid_bp.addSsid5Ghz', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/add-ssid-24ghz-radius", methods=["GET", "POST"])
def addSsid24GhzRadius():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("add-ssid-24ghz-radius.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidName = request.form["ssid_name"]
            vlan = request.form["vlan"]
            bridgeGroup = request.form["bridge_group_id"]
            radioId = request.form["radio_sub_id"]
            gigaId = request.form["giga_sub_id"]
            radiusIp = request.form["radius_ip"]
            sharedSecret = bytes(request.form["shared_secret"], 'utf-8')
            authPort = request.form["auth_port"]
            acctPort = request.form["acct_port"]
            radiusTimeout = request.form["radius_timeout"]
            radiusGroup = request.form["radius_group"]
            methodList = request.form["method_list"]
            encryptedSharedSecret = cipherSuite.encrypt(sharedSecret).decode('utf-8')
            conn = cardinalSql()
            addSsid24GhzRadiusCursor = conn.cursor()
            addSsid24GhzRadiusCursor.execute("INSERT INTO ssids_24ghz_radius (ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (ssidName,vlan,bridgeGroup,radioId,gigaId,radiusIp,encryptedSharedSecret,authPort,acctPort,radiusTimeout,radiusGroup,methodList))
            addSsid24GhzRadiusCursor.close()
            conn.commit()
            conn.close()
            status = msgResourceAdded(resource=ssidName)
            return redirect(url_for('cardinal_ssid_bp.addSsid24GhzRadius', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/add-ssid-5ghz-radius", methods=["GET", "POST"])
def addSsid5GhzRadius():
    if request.method == 'GET':
        if session.get("username") is not None:
            status = request.args.get('status')
            return render_template("add-ssid-5ghz-radius.html", status=status)
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidName = request.form["ssid_name"]
            vlan = request.form["vlan"]
            bridgeGroup = request.form["bridge_group_id"]
            radioId = request.form["radio_sub_id"]
            gigaId = request.form["giga_sub_id"]
            radiusIp = request.form["radius_ip"]
            sharedSecret = bytes(request.form["shared_secret"], 'utf-8')
            authPort = request.form["auth_port"]
            acctPort = request.form["acct_port"]
            radiusTimeout = request.form["radius_timeout"]
            radiusGroup = request.form["radius_group"]
            methodList = request.form["method_list"]
            encryptedSharedSecret = cipherSuite.encrypt(sharedSecret).decode('utf-8')
            conn = cardinalSql()
            addSsid5GhzRadiusCursor = conn.cursor()
            addSsid5GhzRadiusCursor.execute("INSERT INTO ssids_5ghz_radius (ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (ssidName,vlan,bridgeGroup,radioId,gigaId,radiusIp,encryptedSharedSecret,authPort,acctPort,radiusTimeout,radiusGroup,methodList))
            addSsid5GhzRadiusCursor.close()
            conn.commit()
            conn.close()
            status = msgResourceAdded(resource=ssidName)
            return redirect(url_for('cardinal_ssid_bp.addSsid5GhzRadius', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/deploy-ssids", methods=["GET"])
def deploySsids():
    if session.get("username") is not None:
        return render_template("deploy-ssids.html")
    else:
        return msgAuthFailed, 401

@cardinal_ssid.route("/deploy-ssids-group", methods=["GET"])
def deploySsidsGroup():
    if session.get("username") is not None:
        return render_template("deploy-ssids-group.html")
    else:
        return msgAuthFailed, 401

@cardinal_ssid.route("/remove-ssids", methods=["GET"])
def removeSsids():
    if session.get("username") is not None:
        return render_template("remove-ssids.html")
    else:
        return msgAuthFailed, 401

@cardinal_ssid.route("/remove-ssids-group", methods=["GET"])
def removeSsidsGroup():
    if session.get("username") is not None:
        return render_template("remove-ssids-group.html")
    else:
        return msgAuthFailed, 401

@cardinal_ssid.route("/delete-ssids", methods=["GET"])
def deleteSsids():
    if session.get("username") is not None:
        return render_template("delete-ssids.html")
    else:
        return msgAuthFailed, 401

@cardinal_ssid.route("/delete-ssid-24ghz", methods=["GET", "POST"])
def deleteSsid24Ghz():
    if request.method == 'GET':
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
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            if len(ssidId) <= 0:
                status = "Please select a valid 2.4GHz SSID."
                return redirect(url_for('cardinal_ssid_bp.deleteSsid24Ghz', status=status))
            conn = cardinalSql()
            deleteSsidNameCursor = conn.cursor()
            deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_24ghz WHERE ap_ssid_id = %s", [ssidId])
            ssidName = deleteSsidNameCursor.fetchone()[0]
            deleteSsidNameCursor.close()
            status = msgResourceDeleted(resource=ssidName)
            try:
                deleteSsidCursor = conn.cursor()
                deleteSsidCursor.execute("DELETE FROM ssids_24ghz WHERE ap_ssid_id = %s", [ssidId])
                deleteSsidCursor.close()
            except MySQLdb.Error as e:
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid24Ghz', status=e))
            else:
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid24Ghz', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/delete-ssid-5ghz", methods=["GET", "POST"])
def deleteSsid5Ghz():
    if request.method == 'GET':
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
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            if len(ssidId) <= 0:
                status = "Please select a valid 5GHz SSID."
                return redirect(url_for('cardinal_ssid_bp.deleteSsid5Ghz', status=status))
            conn = cardinalSql()
            deleteSsidNameCursor = conn.cursor()
            deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_5ghz WHERE ap_ssid_id = %s", [ssidId])
            ssidName = deleteSsidNameCursor.fetchone()[0]
            deleteSsidNameCursor.close()
            status = msgResourceDeleted(resource=ssidName)
            try:
                deleteSsidCursor = conn.cursor()
                deleteSsidCursor.execute("DELETE FROM ssids_5ghz WHERE ap_ssid_id = %s", [ssidId])
                deleteSsidCursor.close()
            except MySQLdb.Error as e:
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid5Ghz', status=e))
            else:
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid5Ghz', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/delete-ssid-24ghz-radius", methods=["GET", "POST"])
def deleteSsid24GhzRadius():
    if request.method == 'GET':
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
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            if len(ssidId) <= 0:
                status = "Please select a valid 2.4GHz RADIUS SSID."
                return redirect(url_for('cardinal_ssid_bp.deleteSsid24GhzRadius', status=status))
            conn = cardinalSql()
            deleteSsidNameCursor = conn.cursor()
            deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [ssidId])
            ssidName = deleteSsidNameCursor.fetchone()[0]
            deleteSsidNameCursor.close()
            status = msgResourceDeleted(resource=ssidName)
            try:
                deleteSsidCursor = conn.cursor()
                deleteSsidCursor.execute("DELETE FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [ssidId])
                deleteSsidCursor.close()
            except MySQLdb.Error as e:
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid24GhzRadius', status=status))
            else:
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid24GhzRadius', status=status))
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/delete-ssid-5ghz-radius", methods=["GET", "POST"])
def deleteSsid5GhzRadius():
    if request.method == 'GET':
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
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get("username") is not None:
            ssidId = request.form["ssid_id"]
            if len(ssidId) <= 0:
                status = "Please select a valid 5GHz RADIUS SSID."
                return redirect(url_for('cardinal_ssid_bp.deleteSsid5GhzRadius', status=status))
            conn = cardinalSql()
            deleteSsidNameCursor = conn.cursor()
            deleteSsidNameCursor.execute("SELECT ap_ssid_name FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [ssidId])
            ssidName = deleteSsidNameCursor.fetchone()[0]
            deleteSsidNameCursor.close()
            status = "{} was successfully deleted!".format(ssidName)
            try:
                deleteSsidCursor = conn.cursor()
                deleteSsidCursor.execute("DELETE FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [ssidId])
                deleteSsidCursor.close()
            except MySQLdb.Error as e:
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid5GhzRadius', status=status))
            else:
                conn.commit()
                conn.close()
                return redirect(url_for('cardinal_ssid_bp.deleteSsid5GhzRadius', status=status))
        else:
            return msgAuthFailed, 401
