#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2023 Cardinal Contributors

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

from cardinal.system.common import jsonResponse
from cardinal.system.common import Ssid24Ghz
from cardinal.system.common import Ssid5Ghz
from cardinal.system.common import Ssid24GhzRadius
from cardinal.system.common import Ssid5GhzRadius
from cardinal.system.common import msgAuthFailed
from cardinal.system.common import msgResourceAdded
from cardinal.system.common import msgResourceDeleted
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_ssid = Blueprint('cardinal_ssid_bp', __name__)

@cardinal_ssid.route("/api/v1/ssids/24ghz", methods=["GET", "POST", "DELETE"])
def ssid24Ghz():
    '''
    /api/v1/ssids/24ghz is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    2.4GHz SSIDs. Creating a 2.4GHz SSID requires
    a POST request, listing all 2.4GHz SSIDs requires a GET request,
    and deleting a 2.4GHz SSID requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            # TODO: Remove this and have JavaScript handle.
            # Accommodates for lack of PUT/PATCH/DELETE support in HTML forms (specifically for Cardinal UI)
            # See: https://stackoverflow.com/a/5366062
            if request.args.get('method')== "DELETE":
                try:
                    if "ssid_id" in request.args:
                        ssidId = request.args.get('ssid_id')

                        # Check if access point with specified id exists
                        ssidCheck = Ssid24Ghz().info(id=ssidId, struct="dict")
                        if len(ssidCheck) == 0:
                            return jsonResponse(level="ERROR", message="2.4GHz SSID with specified id does not exist."), 404
                        else:
                            ssidName = Ssid24Ghz().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                        Ssid24Ghz().delete(id=ssidId)

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
            else:
                return Ssid24Ghz().info()
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get('username') is not None:
                ssidName = request.form["ssid_name"]
                vlan = request.form["vlan"]
                wpa2Psk = request.form["wpa2_psk"]
                bridgeGroup = request.form["bridge_group_id"]
                radioId = request.form["radio_sub_id"]
                gigaId = request.form["giga_sub_id"]
                status = msgResourceAdded(resource=ssidName)

                try:
                    ssidCreationResult = Ssid24Ghz().add(name=ssidName, vlan=vlan, wpa2=wpa2Psk, bridgeGroup=bridgeGroup, \
                    radioId=radioId, gigaId=gigaId)

                    # Return an HTTP 400 if 2.4GHz SSID with specified name already exists
                    if ssidCreationResult is not None:
                        return jsonResponse(level="ERROR", message=ssidCreationResult), 400

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return Ssid24Ghz().info(name=ssidName), 201
        else:
            return msgAuthFailed, 401
    elif request.method == 'DELETE':
        if session.get('username') is not None:
            try:
                if "ap_ssid_id" in request.form:
                    ssidId = request.form["ap_ssid_id"]

                    # Check if 2.4GHz SSID with specified id exists
                    ssidCheck = Ssid24Ghz().info(id=ssidId, struct="dict")
                    if len(ssidCheck) == 0:
                        return "ERROR: 2.4GHz SSID with specified id does not exist.", 404
                    else:
                        ssidName = Ssid24Ghz().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                    status = msgResourceDeleted(resource=ssidName)
                    Ssid24Ghz().delete(id=ssidId)

                elif "ap_ssid_name" in request.form:
                    ssidName = request.form["ap_ssid_name"]
                    status = msgResourceDeleted(resource=ssidName)
                    Ssid24Ghz().delete(name=ssidName)
                    
            except Exception as e:
                return jsonResponse(level="ERROR", message=e), 400
            else:
                return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/api/v1/ssids/24ghz/<int:id>", methods=["GET"])
def ssid24GhzById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            ssidCheck = Ssid24Ghz().info(id=id, struct="dict")
            if len(ssidCheck) == 0:
                return "ERROR: 2.4GHz SSID with specified id does not exist.", 404
            else:
                return Ssid24Ghz().info(id=id)
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/api/v1/ssids/24ghz_radius", methods=["GET", "POST", "DELETE"])
def ssid24GhzRadius():
    '''
    /api/v1/ssids/24ghz_radius is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    2.4GHz RADIUS SSIDs. Creating a 2.4GHz RADIUS SSID requires
    a POST request, listing all 2.4GHz RADIUS SSIDs requires a GET request,
    and deleting a 2.4GHz RADIUS SSID requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            # TODO: Remove this and have JavaScript handle.
            # Accommodates for lack of PUT/PATCH/DELETE support in HTML forms (specifically for Cardinal UI)
            # See: https://stackoverflow.com/a/5366062
            if request.args.get('method') == "DELETE":
                try:
                    if "ssid_id" in request.args:
                        ssidId = request.args.get('ssid_id')

                        # Check if 2.4GHz RADIUS SSID with specified id exists
                        ssidCheck = Ssid24GhzRadius().info(id=ssidId, struct="dict")
                        if len(ssidCheck) == 0:
                            return jsonResponse(level="ERROR", message="2.4GHz RADIUS SSID with specified id does not exist."), 404
                        else:
                            ssidName = Ssid24GhzRadius().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                        Ssid24GhzRadius().delete(id=ssidId)

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
            else:
                return Ssid24GhzRadius().info()
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get('username') is not None:
                ssidName = request.form["ssid_name"]
                vlan = request.form["vlan"]
                bridgeGroup = request.form["bridge_group_id"]
                radioId = request.form["radio_sub_id"]
                gigaId = request.form["giga_sub_id"]
                radiusIp = request.form["radius_ip"]
                sharedSecret = request.form["shared_secret"]
                authPort = request.form["auth_port"]
                acctPort = request.form["acct_port"]
                radiusTimeout = request.form["radius_timeout"]
                radiusGroup = request.form["radius_group"]
                methodList = request.form["method_list"]

                try:
                    ssidCreationResult = Ssid24GhzRadius().add(name=ssidName, vlan=vlan, bridgeGroup=bridgeGroup, \
                    radioId=radioId, gigaId=gigaId, radiusIp=radiusIp, sharedSecret=sharedSecret, authPort=authPort, \
                    acctPort=acctPort, radiusTimeout=radiusTimeout, radiusGroup=radiusGroup, methodList=methodList)

                    # Return an HTTP 400 if 2.4GHz RADIUS SSID with specified name already exists
                    if ssidCreationResult is not None:
                        return jsonResponse(level="ERROR", message=ssidCreationResult), 400

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return Ssid24GhzRadius().info(name=ssidName), 201
        else:
            return msgAuthFailed, 401
    elif request.method == 'DELETE':
        if session.get('username') is not None:
            try:
                if "ap_ssid_id" in request.form:
                    ssidId = request.form["ap_ssid_id"]

                    # Check if 2.4GHz RADIUS SSID with specified id exists
                    ssidCheck = Ssid24GhzRadius().info(id=ssidId, struct="dict")
                    if len(ssidCheck) == 0:
                        return "ERROR: 2.4GHz RADIUS SSID with specified id does not exist.", 404
                    else:
                        ssidName = Ssid24GhzRadius().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                    status = msgResourceDeleted(resource=ssidName)
                    Ssid24GhzRadius().delete(id=ssidId)

                elif "ap_ssid_name" in request.form:
                    ssidName = request.form["ap_ssid_name"]
                    status = msgResourceDeleted(resource=ssidName)
                    Ssid24GhzRadius().delete(name=ssidName)
                    
            except Exception as e:
                return jsonResponse(level="ERROR", message=e), 400
            else:
                return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/api/v1/ssids/24ghz_radius/<int:id>", methods=["GET"])
def ssid24GhzRadiusById(id):
    '''
    /api/v1/ssids/24ghz_radius is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            ssidCheck = Ssid24GhzRadius().info(id=id, struct="dict")
            if len(ssidCheck) == 0:
                return "ERROR: 2.4GHz RADIUS SSID with specified id does not exist.", 404
            else:
                return Ssid24GhzRadius().info(id=id)
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/api/v1/ssids/5ghz", methods=["GET", "POST", "DELETE"])
def ssid5Ghz():
    '''
    /api/v1/ssids/5ghz is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    5GHz SSIDs. Creating a 5GHz SSID requires
    a POST request, listing all 5GHz SSIDs requires a GET request,
    and deleting a 5GHz SSID requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            # TODO: Remove this and have JavaScript handle.
            # Accommodates for lack of PUT/PATCH/DELETE support in HTML forms (specifically for Cardinal UI)
            # See: https://stackoverflow.com/a/5366062
            if request.args.get('method')== "DELETE":
                try:
                    if "ssid_id" in request.args:
                        ssidId = request.args.get('ssid_id')

                        # Check if access point with specified id exists
                        ssidCheck = Ssid5Ghz().info(id=ssidId, struct="dict")
                        if len(ssidCheck) == 0:
                            return jsonResponse(level="ERROR", message="5GHz SSID with specified id does not exist."), 404
                        else:
                            ssidName = Ssid5Ghz().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                        Ssid5Ghz().delete(id=ssidId)

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
            else:
                return Ssid5Ghz().info()
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get('username') is not None:
                ssidName = request.form["ssid_name"]
                vlan = request.form["vlan"]
                wpa2Psk = request.form["wpa2_psk"]
                bridgeGroup = request.form["bridge_group_id"]
                radioId = request.form["radio_sub_id"]
                gigaId = request.form["giga_sub_id"]
                status = msgResourceAdded(resource=ssidName)

                try:
                    ssidCreationResult = Ssid5Ghz().add(name=ssidName, vlan=vlan, wpa2=wpa2Psk, bridgeGroup=bridgeGroup, \
                    radioId=radioId, gigaId=gigaId)

                    # Return an HTTP 400 if 5GHz SSID with specified name already exists
                    if ssidCreationResult is not None:
                        return jsonResponse(level="ERROR", message=ssidCreationResult), 400

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return Ssid5Ghz().info(name=ssidName), 201
        else:
            return msgAuthFailed, 401
    elif request.method == 'DELETE':
        if session.get('username') is not None:
            try:
                if "ap_ssid_id" in request.form:
                    ssidId = request.form["ap_ssid_id"]

                    # Check if 5GHz SSID with specified id exists
                    ssidCheck = Ssid5Ghz().info(id=ssidId, struct="dict")
                    if len(ssidCheck) == 0:
                        return "ERROR: 5GHz SSID with specified id does not exist.", 404
                    else:
                        ssidName = Ssid5Ghz().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                    status = msgResourceDeleted(resource=ssidName)
                    Ssid5Ghz().delete(id=ssidId)

                elif "ap_ssid_name" in request.form:
                    ssidName = request.form["ap_ssid_name"]
                    status = msgResourceDeleted(resource=ssidName)
                    Ssid5Ghz().delete(name=ssidName)
                    
            except Exception as e:
                return jsonResponse(level="ERROR", message=e), 400
            else:
                return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/api/v1/ssids/5ghz/<int:id>", methods=["GET"])
def ssid5GhzById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            ssidCheck = Ssid5Ghz().info(id=id, struct="dict")
            if len(ssidCheck) == 0:
                return "ERROR: 5GHz SSID with specified id does not exist.", 404
            else:
                return Ssid5Ghz().info(id=id)
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/api/v1/ssids/5ghz_radius", methods=["GET", "POST", "DELETE"])
def ssid5GhzRadius():
    '''
    /api/v1/ssids/5ghz_radius is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    5GHz RADIUS SSIDs. Creating a 5GHz RADIUS SSID requires
    a POST request, listing all 5GHz RADIUS SSIDs requires a GET request,
    and deleting a 5GHz RADIUS SSID requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            # TODO: Remove this and have JavaScript handle.
            # Accommodates for lack of PUT/PATCH/DELETE support in HTML forms (specifically for Cardinal UI)
            # See: https://stackoverflow.com/a/5366062
            if request.args.get('method') == "DELETE":
                try:
                    if "ssid_id" in request.args:
                        ssidId = request.args.get('ssid_id')

                        # Check if 5GHz RADIUS SSID with specified id exists
                        ssidCheck = Ssid5GhzRadius().info(id=ssidId, struct="dict")
                        if len(ssidCheck) == 0:
                            return jsonResponse(level="ERROR", message="5GHz RADIUS SSID with specified id does not exist."), 404
                        else:
                            ssidName = Ssid5GhzRadius().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                        Ssid5GhzRadius().delete(id=ssidId)

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
            else:
                return Ssid5GhzRadius().info()
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get('username') is not None:
                ssidName = request.form["ssid_name"]
                vlan = request.form["vlan"]
                bridgeGroup = request.form["bridge_group_id"]
                radioId = request.form["radio_sub_id"]
                gigaId = request.form["giga_sub_id"]
                radiusIp = request.form["radius_ip"]
                sharedSecret = request.form["shared_secret"]
                authPort = request.form["auth_port"]
                acctPort = request.form["acct_port"]
                radiusTimeout = request.form["radius_timeout"]
                radiusGroup = request.form["radius_group"]
                methodList = request.form["method_list"]

                try:
                    ssidCreationResult = Ssid5GhzRadius().add(name=ssidName, vlan=vlan, bridgeGroup=bridgeGroup, \
                    radioId=radioId, gigaId=gigaId, radiusIp=radiusIp, sharedSecret=sharedSecret, authPort=authPort, \
                    acctPort=acctPort, radiusTimeout=radiusTimeout, radiusGroup=radiusGroup, methodList=methodList)

                    # Return an HTTP 400 if 5GHz RADIUS SSID with specified name already exists
                    if ssidCreationResult is not None:
                        return jsonResponse(level="ERROR", message=ssidCreationResult), 400

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return Ssid5GhzRadius().info(name=ssidName), 201
        else:
            return msgAuthFailed, 401
    elif request.method == 'DELETE':
        if session.get('username') is not None:
            try:
                if "ap_ssid_id" in request.form:
                    ssidId = request.form["ap_ssid_id"]

                    # Check if 5GHz RADIUS SSID with specified id exists
                    ssidCheck = Ssid5GhzRadius().info(id=ssidId, struct="dict")
                    if len(ssidCheck) == 0:
                        return "ERROR: 5GHz RADIUS SSID with specified id does not exist.", 404
                    else:
                        ssidName = Ssid5GhzRadius().info(id=ssidId, struct="dict")[0]["ap_ssid_name"]

                    status = msgResourceDeleted(resource=ssidName)
                    Ssid5GhzRadius().delete(id=ssidId)

                elif "ap_ssid_name" in request.form:
                    ssidName = request.form["ap_ssid_name"]
                    status = msgResourceDeleted(resource=ssidName)
                    Ssid5GhzRadius().delete(name=ssidName)
                    
            except Exception as e:
                return jsonResponse(level="ERROR", message=e), 400
            else:
                return jsonResponse(level="INFO", message="{} deleted successfully".format(ssidName)), 200
        else:
            return msgAuthFailed, 401

@cardinal_ssid.route("/api/v1/ssids/5ghz_radius/<int:id>", methods=["GET"])
def ssid5GhzRadiusById(id):
    '''
    /api/v1/ssids/5ghz_radius is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            ssidCheck = Ssid5GhzRadius().info(id=id, struct="dict")
            if len(ssidCheck) == 0:
                return "ERROR: 5GHz RADIUS SSID with specified id does not exist.", 404
            else:
                return Ssid5GhzRadius().info(id=id)
        else:
            return msgAuthFailed, 401
