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

from cardinal.system.common import AccessPoint
from cardinal.system.common import AccessPointGroup
from cardinal.system.common import Ssid24Ghz
from cardinal.system.common import Ssid5Ghz
from cardinal.system.common import Ssid24GhzRadius
from cardinal.system.common import Ssid5GhzRadius
from cardinal.system.common import msgAuthFailed
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import session
from flask import url_for

cardinal_visuals = Blueprint('cardinal_visuals_bp', __name__)

@cardinal_visuals.route("/api/v1/metrics", methods=["GET"])
def cardinalMetrics():
    if session.get("username") is not None:
        totalAps = len(AccessPoint().info(struct="dict"))
        totalApGroups = len(AccessPointGroup().info(struct="dict"))
        totalSsids24Ghz = len(Ssid24Ghz().info(struct="dict"))
        totalSsids5Ghz = len(Ssid5Ghz().info(struct="dict"))
        totalSsids24GhzRadius = len(Ssid24GhzRadius().info(struct="dict"))
        totalSsids5GhzRadius = len(Ssid5GhzRadius().info(struct="dict"))

        # Calculate total number of SSIDs registered
        totalSsids = totalSsids24Ghz + totalSsids5Ghz + totalSsids24GhzRadius + totalSsids5GhzRadius

        # TODO: Maybe it would be better to implement a totalClients count
        # at the AccessPoint() level? Not sure if this is the best way.
        # Calculate total number of clients associated
        totalApClients = AccessPoint().info(struct="dict")

        # Store client totals in a tuple for sum()
        storeTotalClients = ()

        for a in totalApClients:
            storeTotalClients = storeTotalClients + (int(a["ap_total_clients"]),)

        totalClients = sum(storeTotalClients)
        
        # Populate dict() and then convert to JSON
        metricsDict = dict(access_points=totalAps, access_point_groups=totalApGroups, total_clients=totalClients, total_ssids=totalSsids, ssids_24ghz=totalSsids24Ghz, ssids_5ghz=totalSsids5Ghz,
                        ssids_24ghz_radius=totalSsids24GhzRadius, ssids_5ghz_radius=totalSsids5GhzRadius)
        
        return metricsDict

@cardinal_visuals.route("/total-clients", methods=["GET"])
def totalClients():
    if session.get("username") is not None:
        return render_template("total-clients.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/total-aps", methods=["GET"])
def totalAps():
    if session.get("username") is not None:
        return render_template("total-aps.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/total-ssids", methods=["GET"])
def totalSsids():
    if session.get("username") is not None:
        return render_template("total-ssids.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/total-ap-groups", methods=["GET"])
def totalApGroups():
    if session.get("username") is not None:
        return render_template("total-ap-groups.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/total-ap-bandwidth", methods=["GET"])
def totalApBandwidth():
    if session.get("username") is not None:
        return render_template("total-ap-bandwidth.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/total-ap-clients", methods=["GET"])
def totalApClients():
    if session.get("username") is not None:
        return render_template("total-ap-clients.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/ap-ip-address", methods=["GET"])
def apIpAddress():
    if session.get("username") is not None:
        return render_template("ap-ip-address.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/ap-model", methods=["GET"])
def apModel():
    if session.get("username") is not None:
        return render_template("ap-model.html")
    else:
        return msgAuthFailed, 401

@cardinal_visuals.route("/total-ap-group-clients", methods=["GET"])
def totalApGroupClients():
    if session.get("username") is not None:
        apGroupId = session.get("apGroupId")
        totalApGroupClients = AccessPointGroup().info(id=apGroupId, struct="dict")[0]["ap_group_total_clients"]
        return render_template('total-ap-group-clients.html', totalApGroupClients=totalApGroupClients)
    else:
        return msgAuthFailed, 401