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

import scout_auth
import scout_env
import time

# SCOUT SSID COMMAND FUNCTIONS

def scoutCreateSsid24(ip, username, password, ssid, wpa2Pass, vlan, bridgeGroup, radioSub, gigaSub):
    """Function that deploys a 2.4GHz SSID to an AP
    using user provided arguments.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    jinjaEnv = scout_env.scoutJinjaEnv()
    commandDebug = scout_env.scoutEnv()
    ssid = ssid
    wpa2Pass = wpa2Pass
    vlan = vlan
    bridgeGroup = bridgeGroup
    radioSub = radioSub
    gigaSub = gigaSub
    cmdTemplate = jinjaEnv.get_template("scout_create_ssid_24")
    cmds = cmdTemplate.render(password=password,ssid=ssid,wpa2Pass=wpa2Pass,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Deploying 2.4GHz SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        if commandDebug == "on":
            commands = channel.recv(65535)
            print(commands)
        time.sleep(.10)
    scoutSsh.close()

def scoutCreateSsid5(ip, username, password, ssid, wpa2Pass, vlan, bridgeGroup, radioSub, gigaSub):
    """Function that deploys a 5GHz SSID to an AP
    using user provided arguments.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    jinjaEnv = scout_env.scoutJinjaEnv()
    commandDebug = scout_env.scoutEnv()
    ssid = ssid
    wpa2Pass = wpa2Pass
    vlan = vlan
    bridgeGroup = bridgeGroup
    radioSub = radioSub
    gigaSub = gigaSub
    cmdTemplate = jinjaEnv.get_template("scout_create_ssid_5")
    cmds = cmdTemplate.render(password=password,ssid=ssid,wpa2Pass=wpa2Pass,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Deploying 5GHz SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        if commandDebug == "on":
            commands = channel.recv(65535)
            print(commands)
        time.sleep(.10)
    scoutSsh.close()

def scoutCreateSsid24Radius(ip, username, password, ssid, vlan, bridgeGroup, radioSub, gigaSub, radiusIp, sharedSecret, authPort, acctPort, radiusTimeout, radiusGroup, methodList):
    """Function that deploys a 2.4GHz 802.1x SSID to an 
    AP using user provided arguments.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    jinjaEnv = scout_env.scoutJinjaEnv()
    commandDebug = scout_env.scoutEnv()
    ssid = ssid
    vlan = vlan
    bridgeGroup = bridgeGroup
    radioSub = radioSub
    gigaSub = gigaSub
    radiusIp = radiusIp
    sharedSecret = sharedSecret
    authPort = authPort
    acctPort = acctPort
    radiusTimeout = radiusTimeout
    radiusGroup = radiusGroup
    methodList = methodList
    cmdTemplate = jinjaEnv.get_template("scout_create_radius_ssid_24")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub,radiusIp=radiusIp,sharedSecret=sharedSecret,authPort=authPort,acctPort=acctPort,radiusTimeout=radiusTimeout,radiusGroup=radiusGroup,methodList=methodList)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Deploying 2.4GHz RADIUS SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        if commandDebug == "on":
            commands = channel.recv(65535)
            print(commands)
        time.sleep(.10)
    scoutSsh.close()

def scoutCreateSsid5Radius(ip, username, password, ssid, vlan, bridgeGroup, radioSub, gigaSub, radiusIp, sharedSecret, authPort, acctPort, radiusTimeout, radiusGroup, methodList):
    """Function that deploys a 5GHz 802.1x SSID to an
    AP using user provided arguments.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip,username=username,password=password)
    jinjaEnv = scout_env.scoutJinjaEnv()
    commandDebug = scout_env.scoutEnv()
    ssid = ssid
    vlan = vlan
    bridgeGroup = bridgeGroup
    radioSub = radioSub
    gigaSub = gigaSub
    radiusIp = radiusIp
    sharedSecret = sharedSecret
    authPort = authPort
    acctPort = acctPort
    radiusTimeout = radiusTimeout
    radiusGroup = radiusGroup
    methodList = methodList
    cmdTemplate = jinjaEnv.get_template("scout_create_radius_ssid_5")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub,radiusIp=radiusIp,sharedSecret=sharedSecret,authPort=authPort,acctPort=acctPort,radiusTimeout=radiusTimeout,radiusGroup=radiusGroup,methodList=methodList)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Deploying 5GHz RADIUS SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        if commandDebug == "on":
            commands = channel.recv(65535)
            print(commands)
        time.sleep(.10)
    scoutSsh.close()

def scoutDeleteSsid24(ip, username, password, ssid, vlan, radioSub, gigaSub):
    """Function that deletes an existing 2.4GHz SSID from
    an AP.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    jinjaEnv = scout_env.scoutJinjaEnv()
    commandDebug = scout_env.scoutEnv()
    ssid = ssid
    vlan = vlan
    radioSub = radioSub
    gigaSub = gigaSub
    cmdTemplate = jinjaEnv.get_template("scout_delete_ssid_24")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Removing 2.4GHz SSID {0} from {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        if commandDebug == "on":
            commands = channel.recv(65535)
            print(commands)
        time.sleep(.10)
    scoutSsh.close()

def scoutDeleteSsid5(ip, username, password, ssid, vlan, radioSub, gigaSub):
    """Function that deletes an existing 5GHz SSID from an
    AP.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    jinjaEnv = scout_env.scoutJinjaEnv()
    commandDebug = scout_env.scoutEnv()
    ssid = ssid
    vlan = vlan
    radioSub = radioSub
    gigaSub = gigaSub
    cmdTemplate = jinjaEnv.get_template("scout_delete_ssid_5")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Removing 5GHz SSID {0} from {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        if commandDebug == "on":
            commands = channel.recv(65535)
            print(commands)
        time.sleep(.10)
    scoutSsh.close()
