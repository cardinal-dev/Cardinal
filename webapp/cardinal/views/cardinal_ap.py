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

from cardinal.system.common import AccessPoint
from cardinal.system.common import AsyncOpsManager
from cardinal.system.common import msgAuthFailed
from cardinal.system.common import msgResourceAdded
from cardinal.system.common import msgSpecifyValidAp
from cardinal.system.common import jsonResponse
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_ap = Blueprint('cardinal_ap_bp', __name__)

# Establish connection to AsyncOpsManager()
job = AsyncOpsManager()

@cardinal_ap.route("/api/v1/access_points", methods=["GET", "POST", "DELETE"])
def accessPoints():
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            # TODO: Remove this and have JavaScript process.
            # Accommodates for lack of PUT/PATCH/DELETE support in HTML forms (specifically for Cardinal UI)
            # See: https://stackoverflow.com/a/5366062
            if request.args.get('method') == "DELETE":
                try:
                    if "ap_id" in request.args:
                        apId = request.args.get('ap_id')

                        # Check if access point with specified id exists
                        apCheck = AccessPoint().info(id=apId, struct="dict")
                        if len(apCheck) == 0:
                            return jsonResponse(level="ERROR", message="Access point with specified id does not exist"), 404
                        else:
                            apName = AccessPoint().info(id=apId, struct="dict")[0]["ap_name"]

                        # Delete the specified access point by id
                        deleteAp = AccessPoint().delete(id=apId)

                        # Handle MySQL issues (particularly around foreign key constraints)
                        # See: https://mariadb.com/kb/en/mariadb-error-codes/#1451
                        if deleteAp is not None:
                            if "1451" in deleteAp:
                                return jsonResponse(level="ERROR", message="Please ensure the specified access point doesn't have any resources associated"), 400
                        
                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return jsonResponse(level="INFO", message="{} deleted successfully".format(apName)), 200
            else:
                return AccessPoint().info()
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get('username') is not None:
                apName = request.form["ap_name"]
                apIp = request.form["ap_ip"]
                apSubnetMask = request.form["ap_subnetmask"]
                apSshPort = request.form["ssh_port"]
                sshUsername = request.form["ssh_username"]
                sshPassword = request.form["ssh_password"]
                community = request.form["community"]

                try:
                    # Check if POST request has a group_id. If not, act accordingly
                    if "group_id" in request.form:
                        if len(request.form["group_id"]) >= 1:
                            apGroupId = request.form["group_id"]
                            apCreationResult = AccessPoint().add(name=apName,ip=apIp,subnetMask=apSubnetMask,sshPort=apSshPort,username=sshUsername,\
                            password=sshPassword,community=community,groupId=apGroupId)
                        else:
                            apCreationResult = AccessPoint().add(name=apName,ip=apIp,subnetMask=apSubnetMask,sshPort=apSshPort,username=sshUsername,password=sshPassword,community=community)
                    else:
                        apCreationResult = AccessPoint().add(name=apName,ip=apIp,subnetMask=apSubnetMask,sshPort=apSshPort,username=sshUsername,password=sshPassword,community=community)

                    # Return an HTTP 400 if access point with specified name already exists
                    if apCreationResult is not None:
                        return jsonResponse(level="ERROR", message=apCreationResult), 400

                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return AccessPoint().info(name=apName), 201
        else:
            return msgAuthFailed, 401
    elif request.method == 'DELETE':
        if session.get('username') is not None:
            try:
                if "ap_id" in request.form:
                    apId = request.form["ap_id"]

                    # Check if access point with specified id exists
                    apCheck = AccessPoint().info(id=apId, struct="dict")
                    if len(apCheck) == 0:
                        return "ERROR: Access point with specified id does not exist.", 404
                    else:
                        apName = AccessPoint().info(id=apId, struct="dict")[0]["ap_name"]

                    # Delete the specified access point by id
                    deleteAp = AccessPoint().delete(id=apId)

                    # Handle MySQL issues (particularly around foreign key constraints)
                    if deleteAp is not None:
                        if "1451" in deleteAp:
                            return jsonResponse(level="ERROR", message="Please ensure the specified access point doesn't have any resources associated"), 400

                elif "ap_name" in request.form:
                    apName = request.form["ap_name"]
                    AccessPoint().delete(name=apName)
                    
            except Exception as e:
                return jsonResponse(level="ERROR", message=e), 400
            else:
                return jsonResponse(level="INFO", message="{} deleted successfully".format(apName)), 200
        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>", methods=["GET"])
def accessPointById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            apCheck = AccessPoint().info(id=id, struct="dict")
            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                return AccessPoint().info(id=id)
        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/change_ip", methods=["POST"])
def changeAccessPointIPById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)
            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                apId = request.form["ap_id"]
                newApIp = request.form["ap_new_ip"]
                newApSubnetMask = request.form["ap_subnetmask"]
                # Send change access point IP job to Redis queue
                result = job.run(func=accessPoint.changeIp, args=dict(id=apId, newIp=newApIp, subnetMask=newApSubnetMask))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Change access point IP job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Change access point IP job failed", reference=result._status), 409
        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/change_hostname", methods=["POST"])
def changeAccessPointNameById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                hostname = request.form["ap_name"]
                # Send change access point IP job to Redis queue
                result = job.run(func=accessPoint.changeHostname, args=dict(id=id, hostname=hostname))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Change access point hostname job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Change access point hostname job failed", reference=result._status), 409
        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/fetcher", methods=["POST"])
def fetchAccessPointInfoById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                # Send fetch AP info job to Redis queue
                result = job.run(func=accessPoint.fetchInfo, args=dict(id=id))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Fetch AP info job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Fetch AP info job failed", reference=result._status), 409
        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/tftp", methods=["POST"])
def tftpBackupByApId(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                tftpIp = request.form["tftp_ip"]
                result = job.run(func=accessPoint.tftpBackup, args=dict(id=id, tftpIp=tftpIp))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="TFTP backup job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="TFTP backup job failed", reference=result._status), 409
        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/http/<status>", methods=["POST"])
def manageHttpByApId(id, status):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                result = job.run(func=accessPoint.manageHttp, args=dict(id=id, status=status))
                
                if status == "enable":
                    if result._status == 'queued':
                        return jsonResponse(level="INFO", message="Enable HTTP job successfully dispatched", reference=result._id), 201
                    else:
                        return jsonResponse(level="ERROR", message="Enable HTTP job failed", reference=result._status), 409
                elif status == "disable":
                    if result._status == 'queued':
                        return jsonResponse(level="INFO", message="Disable HTTP job successfully dispatched", reference=result._id), 201
                    else:
                        return jsonResponse(level="ERROR", message="Disable HTTP job failed", reference=result._status), 409
                else:
                    return jsonResponse(level="ERROR", message="Invalid HTTP operation status. Please choose from the following: enable, disable"), 400

        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/snmp/<status>", methods=["POST"])
def manageSnmpByApId(id, status):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                result = job.run(func=accessPoint.manageSnmp, args=dict(id=id, status=status))
                
                if status == "enable":
                    if result._status == 'queued':
                        return jsonResponse(level="INFO", message="Enable SNMP job successfully dispatched", reference=result._id), 201
                    else:
                        return jsonResponse(level="ERROR", message="Enable SNMP job failed", reference=result._status), 409
                elif status == "disable":
                    if result._status == 'queued':
                        return jsonResponse(level="INFO", message="Disable SNMP job successfully dispatched", reference=result._id), 201
                    else:
                        return jsonResponse(level="ERROR", message="Disable SNMP job failed", reference=result._status), 409
                else:
                    return jsonResponse(level="ERROR", message="Invalid SNMP operation status. Please choose from the following: enable, disable"), 400

        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/deploy_ssid/24ghz", methods=["POST"])
def deploySsid24GhzById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.deploy24GhzSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Deploy 2.4GHz SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Deploy 2.4GHz SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/deploy_ssid/5ghz", methods=["POST"])
def deploySsid5GhzById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.deploy5GhzSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Deploy 5GHz SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Deploy 5GHz SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401


@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/deploy_ssid/24ghz_radius", methods=["POST"])
def deploySsid24RadiusGhzById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.deploy24GhzRadiusSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Deploy 2.4GHz 802.1x SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Deploy 2.4GHz 802.1x SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401


@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/deploy_ssid/5ghz_radius", methods=["POST"])
def deploySsid5GhzRadiusById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.deploy5GhzRadiusSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Deploy 5GHz 802.1x SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Deploy 5GHz 802.1x SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401


@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/remove_ssid/24ghz", methods=["POST"])
def removeSsid24GhzById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.remove24GhzSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Remove 2.4GHz SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Remove 2.4GHz SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/remove_ssid/5ghz", methods=["POST"])
def removeSsid5GhzById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.remove5GhzSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Remove 5GHz SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Remove 5GHz SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401


@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/remove_ssid/24ghz_radius", methods=["POST"])
def removeSsid24GhzRadiusById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.remove24GhzRadiusSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Remove 2.4GHz 802.1x SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Remove 2.4GHz 802.1x SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401

@cardinal_ap.route("/api/v1/access_points/<int:id>/ops/remove_ssid/5ghz_radius", methods=["POST"])
def removeSsid5GhzRadiusById(id):
    '''
    /api/v1/access_points is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access points. Creating an access point requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'POST':
        if session.get("username") is not None:
            # Initialize AccessPoint() object
            accessPoint = AccessPoint()
            apCheck = accessPoint.info(id=id)

            if len(apCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point with specified id does not exist."), 404
            else:
                ssidId = request.form["ssid_id"]
                result = job.run(func=accessPoint.remove5GhzRadiusSsid, args=dict(id=id, ssidId=ssidId))
                
                if result._status == 'queued':
                    return jsonResponse(level="INFO", message="Remove 5GHz 802.1x SSID job successfully dispatched", reference=result._id), 201
                else:
                    return jsonResponse(level="ERROR", message="Remove 5GHz 802.1x SSID job failed", reference=result._status), 409

        else:
            return msgAuthFailed, 401