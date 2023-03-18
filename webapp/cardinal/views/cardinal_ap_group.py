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

from cardinal.system.common import AccessPointGroup
from cardinal.system.common import jsonResponse
from cardinal.system.common import msgAuthFailed
from cardinal.system.common import msgResourceAdded
from cardinal.system.common import msgResourceDeleted
from cardinal.system.common import msgSpecifyValidApGroup
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for

cardinal_ap_group = Blueprint('cardinal_ap_group_bp', __name__)

@cardinal_ap_group.route("/api/v1/access_point_groups", methods=["GET", "POST", "DELETE"])
def accessPointGroups():
    '''
    /api/v1/access_point_groups is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access point groups. Creating an access point group requires
    a POST request, listing all access point groups requires a GET request,
    and deleting an access point group requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            # TODO: Remove this and have JavaScript handle.
            # Accommodates for lack of PUT/PATCH/DELETE support in HTML forms (specifically for Cardinal UI)
            # See: https://stackoverflow.com/a/5366062
            if request.args.get('method')== "DELETE":
                try:
                    if "ap_group_id" in request.args:
                        apGroupId = request.args.get('ap_group_id')

                        # Check if access point group with specified id exists
                        apGroupCheck = AccessPointGroup().info(id=apGroupId, struct="dict")
                        if len(apGroupCheck) == 0 or apGroupCheck[0]["ap_group_id"] is None:
                            return jsonResponse(level="ERROR", message="Access point group with specified id does not exist."), 404
                        else:
                            apGroupName = AccessPointGroup().info(id=apGroupId, struct="dict")[0]["ap_group_name"]

                        status = msgResourceDeleted(resource=apGroupName)
                        AccessPointGroup().delete(id=apGroupId)
                        
                except Exception as e:
                    return jsonResponse(level="ERROR", message=e), 400
                else:
                    return jsonResponse(level="INFO", message="{} deleted successfully".format(apGroupName)), 200
            else:
                return AccessPointGroup().info()
        else:
            return msgAuthFailed, 401
    elif request.method == 'POST':
        if session.get('username') is not None:
            if request.form["ap_group_name"]:
                apGroupName = request.form["ap_group_name"]
                status = msgResourceAdded(resource=apGroupName)
                try:
                    apGroupCreationResult = AccessPointGroup().add(name=apGroupName)

                    # Return an HTTP 400 if access point group with specified name already exists
                    if apGroupCreationResult is not None:
                        return jsonResponse(level="ERROR", message=apGroupCreationResult), 400
        
                except Exception as e:
                    return "ERROR: {}".format(e)
                else:
                    return AccessPointGroup().info(name=apGroupName), 201
        else:
            return msgAuthFailed, 401
    elif request.method == 'DELETE':
        if session.get('username') is not None:
            try:
                if "ap_group_id" in request.form:
                    apGroupId = request.form["ap_group_id"]

                    # Check if access point group with specified id exists
                    apGroupCheck = AccessPointGroup().info(id=apGroupId, struct="dict")
                    if len(apGroupCheck) == 0:
                        return jsonResponse(level="ERROR", message="Access point group with specified id does not exist."), 404
                    else:
                        apGroupName = AccessPointGroup().info(id=apGroupId, struct="dict")[0]["ap_group_name"]

                    status = msgResourceDeleted(resource=apGroupName)
                    AccessPointGroup().delete(id=apGroupId)

                elif "ap_group_name" in request.form:
                    apGroupName = request.form["ap_group_name"]
                    status = msgResourceDeleted(resource=apGroupName)
                    AccessPointGroup().delete(name=apGroupName)
                    
            except Exception as e:
                return jsonResponse(level="ERROR", message=e), 400
            else:
                return jsonResponse(level="INFO", message="{} deleted successfully".format(apGroupName)), 200
        else:
            return msgAuthFailed, 401

@cardinal_ap_group.route("/api/v1/access_point_groups/<int:id>", methods=["GET"])
def accessPointGroupById(id):
    '''
    /api/v1/access_point_groups is an endpoint that allows
    a Cardinal user to create, list, and delete registered
    access point groups. Creating an access point group requires
    a POST request, listing all access points requires a GET request,
    and deleting an access point requires a DELETE request.
    '''
    if request.method == 'GET':
        if session.get("username") is not None:
            apGroupCheck = AccessPointGroup().info(id=id, struct="dict")
            if len(apGroupCheck) == 0:
                return jsonResponse(level="ERROR", message="Access point group with specified id does not exist."), 404
            else:
                return AccessPointGroup().info(id=id)
        else:
            return msgAuthFailed, 401
