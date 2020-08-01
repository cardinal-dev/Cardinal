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

import subprocess
from cardinal.system.cardinal_sys import msgAuthFailed
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_network_toolkit = Blueprint('cardinal_network_toolkit_bp', __name__)

@cardinal_network_toolkit.route("/network-tools", methods=["GET"])
def networkTools():
    if session.get("username") is not None:
        return render_template("network-tools.html")
    else:
        return msgAuthFailed, 401

@cardinal_network_toolkit.route("/tools-output", methods=["GET"])
def networkToolsOutput():
    if session.get("username") is not None:
        commandOutput = request.args.get("commandOutput")
        return render_template("network-tools-output.html", commandOutput=commandOutput)
    else:
        return msgAuthFailed, 401

@cardinal_network_toolkit.route("/do-ping", methods=["POST"])
def doPing():
    if request.method == 'POST':
        if session.get("username") is not None:
            ip = request.form["network_ip"]
            pingArgs = ["ping", "-c", "4", "{}".format(ip)]
            pingCmd = subprocess.Popen(pingArgs, stdout=subprocess.PIPE)
            commandOutput = pingCmd.stdout.read()
            return redirect(url_for('cardinal_network_toolkit_bp.networkToolsOutput', commandOutput=commandOutput.decode('ascii')))
        else:
            return msgAuthFailed, 401

@cardinal_network_toolkit.route("/do-tracert", methods=["POST"])
def doTracert():
    if request.method == 'POST':
        if session.get("username") is not None:
            ip = request.form["network_ip"]
            tracertArgs = ["traceroute", "{}".format(ip)]
            tracertCmd = subprocess.Popen(tracertArgs, stdout=subprocess.PIPE)
            commandOutput = tracertCmd.stdout.read()
            return redirect(url_for('cardinal_network_toolkit_bp.networkToolsOutput', commandOutput=commandOutput.decode('ascii')))
        else:
            return msgAuthFailed, 401

@cardinal_network_toolkit.route("/do-dig", methods=["POST"])
def doDig():
    if request.method == 'POST':
        if session.get("username") is not None:
            ip = request.form["network_ip"]
            digArgs = ["dig", "{}".format(ip)]
            digCmd = subprocess.Popen(digArgs, stdout=subprocess.PIPE)
            commandOutput = digCmd.stdout.read()
            return redirect(url_for('cardinal_network_toolkit_bp.networkToolsOutput', commandOutput=commandOutput.decode('ascii')))
        else:
            return msgAuthFailed, 401

@cardinal_network_toolkit.route("/do-curl", methods=["POST"])
def doCurl():
    if request.method == 'POST':
        if session.get("username") is not None:
            ip = request.form["network_ip"]
            curlArgs = ["curl", "-Is", "{}".format(ip)]
            curlCmd = subprocess.Popen(curlArgs, stdout=subprocess.PIPE)
            commandOutput = curlCmd.stdout.read()
            return redirect(url_for('cardinal_network_toolkit_bp.networkToolsOutput', commandOutput=commandOutput.decode('ascii')))
        else:
            return msgAuthFailed, 401
