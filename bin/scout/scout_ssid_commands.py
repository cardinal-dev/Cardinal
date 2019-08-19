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

import os
import time
import sys
import paramiko
import jinja2
from configparser import ConfigParser

# CARDINAL SETTINGS

cardinalConfigFile = os.environ['CARDINALCONFIG']
cardinalConfig = ConfigParser()
cardinalConfig.read("{}".format(cardinalConfigFile))

# BEGIN CARDINAL SETTING DECLARATIONS

commandDir = cardinalConfig.get('cardinal', 'commanddir')

# CARDINAL SYSTEM VARIABLES

fileLoader = jinja2.FileSystemLoader('{}'.format(commandDir))
env = jinja2.Environment(loader=fileLoader)

# SSH INFORMATION

def sshInfo():
    ip = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    scoutSsh = paramiko.SSHClient()
    scoutSsh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    scoutSsh.connect(ip, port = 22, username = username, password = password, look_for_keys = False, allow_agent = False)
    return ip, username, password, scoutSsh

# Scout Ssid Command Functions

def scoutCreateSsid24():
    """Function that deploys a 2.4GHz SSID to an AP
    using user provided arguments.
    """
    ip, username, password, scoutSsh = sshInfo()
    ssid = sys.argv[5]
    wpa2Pass = sys.argv[6]
    vlan = sys.argv[7]
    bridgeGroup = sys.argv[8]
    radioSub = sys.argv[9]
    gigaSub = sys.argv[10]
    cmdTemplate = env.get_template("scout_create_ssid_24")
    cmds = cmdTemplate.render(password=password,ssid=ssid,wpa2Pass=wpa2Pass,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --create-ssid-24...")
    print("INFO: Deploying 2.4GHz SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutCreateSsid5():
    """Function that deploys a 5GHz SSID to an AP
    using user provided arguments.
    """
    ip, username, password, scoutSsh = sshInfo()
    ssid = sys.argv[5]
    wpa2Pass = sys.argv[6]
    vlan = sys.argv[7]
    bridgeGroup = sys.argv[8]
    radioSub = sys.argv[9]
    gigaSub = sys.argv[10]
    cmdTemplate = env.get_template("scout_create_ssid_5")
    cmds = cmdTemplate.render(password=password,ssid=ssid,wpa2Pass=wpa2Pass,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --create-ssid-5...")
    print("INFO: Deploying 5GHz SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutCreateSsid24Radius():
    """Function that deploys a 2.4GHz 802.1x SSID to an 
    AP using user provided arguments.
    """
    ip, username, password, scoutSsh = sshInfo()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    bridgeGroup = sys.argv[7]
    radioSub = sys.argv[8]
    gigaSub = sys.argv[9]
    radiusIp = sys.argv[10]
    sharedSecret = sys.argv[11]
    authPort = sys.argv[12]
    acctPort = sys.argv[13]
    radiusTimeout = sys.argv[14]
    radiusGroup = sys.argv[15]
    methodList = sys.argv[16]
    cmdTemplate = env.get_template("scout_create_radius_ssid_24")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub,radiusIp=radiusIp,sharedSecret=sharedSecret,authPort=authPort,acctPort=acctPort,radiusTimeout=radiusTimeout,radiusGroup=radiusGroup,methodList=methodList)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --create-ssid-radius-24...")
    print("INFO: Deploying 2.4GHz RADIUS SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutCreateSsid5Radius():
    """Function that deploys a 5GHz 802.1x SSID to an
    AP using user provided arguments.
    """
    ip, username, password, scoutSsh = sshInfo()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    bridgeGroup = sys.argv[7]
    radioSub = sys.argv[8]
    gigaSub = sys.argv[9]
    radiusIp = sys.argv[10]
    sharedSecret = sys.argv[11]
    authPort = sys.argv[12]
    acctPort = sys.argv[13]
    radiusTimeout = sys.argv[14]
    radiusGroup = sys.argv[15]
    methodList = sys.argv[16]
    cmdTemplate = env.get_template("scout_create_radius_ssid_5")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,bridgeGroup=bridgeGroup,radioSub=radioSub,gigaSub=gigaSub,radiusIp=radiusIp,sharedSecret=sharedSecret,authPort=authPort,acctPort=acctPort,radiusTimeout=radiusTimeout,radiusGroup=radiusGroup,methodList=methodList)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --create-ssid-radius-5...")
    print("INFO: Deploying 5GHz RADIUS SSID {0} to {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDeleteSsid24():
    """Function that deletes an existing 2.4GHz SSID from
    an AP.
    """
    ip, username, password, scoutSsh = sshInfo()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    radioSub = sys.argv[7]
    gigaSub = sys.argv[8]
    cmdTemplate = env.get_template("scout_delete_ssid_24")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Removing 2.4GHz SSID {0} from {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDeleteSsid5():
    """Function that deletes an existing 5GHz SSID from an
    AP.
    """
    ip, username, password, scoutSsh = sshInfo()
    ssid = sys.argv[5]
    vlan = sys.argv[6]
    radioSub = sys.argv[7]
    gigaSub = sys.argv[8]
    cmdTemplate = env.get_template("scout_delete_ssid_5")
    cmds = cmdTemplate.render(password=password,ssid=ssid,vlan=vlan,radioSub=radioSub,gigaSub=gigaSub)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Removing 5GHz SSID {0} from {1}...".format(ssid,ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()
