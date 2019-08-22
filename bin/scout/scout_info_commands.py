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
import re
import subprocess
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

# Scout Info Command Functions

def scoutGetArp():
    """Function that opens a SSH connection to the AP
    and runs show ip arp to gather ARP table.
    """
    ip, username, password, scoutSsh = sshInfo()
    stdin, stdout, stderr = scoutSsh.exec_command("show ip arp\n")
    sshOut = stdout.read()
    getArpTable = sshOut.decode('ascii').strip("\n").lstrip()
    scoutSsh.close()
    print(getArpTable)

def scoutGetSpeed():
    """Function that reports speed of Gi0/0 in Mbps."""
    ip, username, password, scoutSsh = sshInfo()
    stdin, stdout, stderr = scoutSsh.exec_command("sho int gi0\n")
    sshOut = stdout.read()
    sshBandwidth = sshOut.decode('ascii').strip("\n").split(",")
    getBandwidth = sshBandwidth[9].strip("Mbps")
    scoutSsh.close()
    print(getBandwidth + "Mbps")

def scoutGetMac():
    """Function that reports back the MAC address of AP."""
    ip, username, password, scoutSsh = sshInfo()
    macAddrRegex = re.compile(r'\w\w\w\w.\w\w\w\w.\w\w\w\w')
    stdin, stdout, stderr = scoutSsh.exec_command("show int gi0\n")
    sshOut = stdout.read()
    intList = sshOut.decode('ascii').strip("\n").split(",")
    getMac = macAddrRegex.search(intList[2]).group(0)
    scoutSsh.close()
    print(getMac)

def scoutCountClients():
    """Function that reports the number of active clients on
    AP via show dot11 associations.
    """
    ip, username, password, scoutSsh = sshInfo()
    stdin, stdout, stderr = scoutSsh.exec_command("show dot11 associations\n")
    sshOut = stdout.read()
    countClient = sshOut.decode('ascii').strip("\n")
    getClient = subprocess.check_output("echo {} | grep -o [0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f] | wc -l".format(countClient), shell=True)
    scoutSsh.close()
    print(getClient.decode('ascii').strip("\n").lstrip())

def scoutGetModel():
    """Function that reports the model ID of AP."""
    ip, username, password, scoutSsh = sshInfo()
    stdin, stdout, stderr = scoutSsh.exec_command("show version\n")
    sshOut = stdout.read()
    getModelString = sshOut.decode('ascii').strip("\n")
    apModelRegex = re.compile(r'\w\w\w\-\w\w\w\w\w\w\w\w\-\w-\w\w')
    getApModel = apModelRegex.search(getModelString).group(0)
    scoutSsh.close()
    print(getApModel)

def scoutGetHostname():
    """Function that retrieves AP hostname via show version."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_get_hostname")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    getHostname = channel.recv(65535).decode('ascii').strip("\n").strip(">").lstrip()
    scoutSsh.close()
    print(getHostname)

def scoutGetLocation():
    """Function that retrieves AP location via show snmp location."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_get_location")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    if channel.recv_ready():
        sshReturn = channel.recv(65535)
        location = sshReturn.decode('ascii').splitlines()
        print(location[4])
    scoutSsh.close()

def scoutGetUsers():
    """Function that retrieves AP users via show users."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_get_users")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    if channel.recv_ready():
        sshReturn = channel.recv(65535)
        users = sshReturn.splitlines()
        for line in users[4:-1]:
            print(line.decode('ascii').strip("\n"))
    scoutSsh.close()

def scoutGetSerial():
    """Function that reports the serial number of AP."""
    ip, username, password, scoutSsh = sshInfo()
    stdin, stdout, stderr = scoutSsh.exec_command("show inventory\n")
    sshOut = stdout.read()
    getSerialString = sshOut.decode('ascii').strip("\n")
    apSerialRegex = re.compile(r'\w\w\w\w\w\w\w\w\w\w\w')
    getApSerial = apSerialRegex.search(getSerialString).group(0)
    scoutSsh.close()
    print(getApSerial)

def scoutGetIosInfo():
    """Function that retrieves AP IOS info via show version."""
    ip, username, password, scoutSsh = sshInfo()
    stdin, stdout, stderr = scoutSsh.exec_command("show version\n")
    sshOut = stdout.read().splitlines()
    getIosInfo = sshOut[0].decode('ascii').strip("\n")
    scoutSsh.close()
    print(getIosInfo)

def scoutGetUptime():
    """Function that retrieves AP uptime via show version."""
    ip, username, password, scoutSsh = sshInfo()
    stdin, stdout, stderr = scoutSsh.exec_command("show version\n")
    sshOut = stdout.read().splitlines()
    getApUptime = sshOut[8].decode('ascii').strip("\n")
    scoutSsh.close()
    print(getApUptime)


