#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2022 Cardinal Contributors

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

from cardinal.system.common import CardinalEnv
from cardinal.views import cardinal_ap_group
from cardinal.views import cardinal_ap_group_ops
from cardinal.views import cardinal_ap
from cardinal.views import cardinal_auth
from cardinal.views import cardinal_forms
from cardinal.views import cardinal_network_toolkit
from cardinal.views import cardinal_ssid
from cardinal.views import cardinal_ssid_ops
from cardinal.views import cardinal_visuals
from datetime import timedelta
from flask import Flask

# Intialize a CardinalEnv() object
cardinalEnv = CardinalEnv()

# Initialize a Flask() object and configure using Cardinal settings
Cardinal = Flask(__name__, static_folder='frontend')
Cardinal.secret_key = cardinalEnv.config()["flaskKey"]
Cardinal.permanent_session_lifetime = int(cardinalEnv.config()["sessionTimeout"])

# Declare Flask blueprints
Cardinal.register_blueprint(cardinal_ap_group.cardinal_ap_group)
Cardinal.register_blueprint(cardinal_ap_group_ops.cardinal_ap_group_ops)
Cardinal.register_blueprint(cardinal_ap.cardinal_ap)
Cardinal.register_blueprint(cardinal_auth.cardinal_auth)
Cardinal.register_blueprint(cardinal_forms.cardinal_forms)
Cardinal.register_blueprint(cardinal_network_toolkit.cardinal_network_toolkit)
Cardinal.register_blueprint(cardinal_ssid.cardinal_ssid)
Cardinal.register_blueprint(cardinal_ssid_ops.cardinal_ssid_ops)
Cardinal.register_blueprint(cardinal_visuals.cardinal_visuals)
