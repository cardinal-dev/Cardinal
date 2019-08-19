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

# Scout Sys Command Functions

def scoutLed():
    """Function that opens a SSH connection to the AP
    and runs led flash 30.
    """
    ip, username, password, scoutSsh = sshInfo()
    print("INFO: Running scout --led on {}...".format(ip))
    stdin, stdout, stderr = scoutSsh.exec_command("led flash 30\n")
    scoutSsh.close()

def scoutChangeIp():
    """Function that identifies SSH info, collects sys args,
    calls the scout_change_ap_ip command set, opens a SSH connection
    to the AP, executes the IP change, terminates the old SSH connection,
    opens a new one, and runs the scout_do_wr command set to save new IP
    change.
    """
    ip, username, password, scoutSsh = sshInfo()
    newIp = sys.argv[5]
    subnetMask = sys.argv[6]
    cmdTemplate = env.get_template("scout_change_ap_ip")
    cmds = cmdTemplate.render(password=password,newIp=newIp,subnetMask=subnetMask)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --change-ip on {}...".format(ip))
    print("INFO: Changing IP from {0} to {1}".format(ip,newIp))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()
    scoutSsh2 = paramiko.SSHClient()
    scoutSsh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    scoutSsh2.connect(newIp, port = 22, username = username, password = password, look_for_keys = False, allow_agent = False)
    cmdTemplate2 = env.get_template("scout_do_wr")
    cmds2 = cmdTemplate2.render(password=password)
    scoutCommands2 = cmds2.splitlines()
    channel2 = scoutSsh2.invoke_shell()
    for command2 in scoutCommands2:
        channel2.send('{}\n'.format(command2))
        time.sleep(.10)
    scoutSsh2.close()

def scoutDisableHttp():
    """Function that disables the HTTP server on AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_disable_ap_http")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --disable-http on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDisableRadius():
    """Function that disables RADIUS on AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_disable_ap_radius")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --disable-radius on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDisableSnmp():
    """Function that disables SNMP on AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_disable_ap_snmp")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --disable-snmp on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutEnableHttp():
    """Function that enables the HTTP server on AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_enable_ap_http")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --enable-http on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutEnableRadius():
    """Function that enables RADIUS on AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_enable_ap_radius")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --enable-radius on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutEnableSnmp():
    """Function that enables SNMP on AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_enable_ap_snmp")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --enable-snmp on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutTftpBackup():
    """Function that performs TFTP backup of AP config."""
    ip, username, password, scoutSsh = sshInfo()
    tftpIp = sys.argv[5]
    cmdTemplate = env.get_template("scout_do_tftp_backup")
    cmds = cmdTemplate.render(password=password,tftpIp=tftpIp)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --tftp-backup on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDoWr():
    """Function that performs write command on AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_do_wr")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --wr on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutWriteDefault():
    """Function that wipes AP memory back to default."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_write_default")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --erase on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutChangeName():
    """Function that changes the hostname of AP."""
    ip, username, password, scoutSsh = sshInfo()
    apName = sys.argv[5]
    cmdTemplate = env.get_template("scout_change_ap_name")
    cmds = cmdTemplate.render(apName=apName,password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --change-name on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDoReboot():
    """Function that reboots AP."""
    ip, username, password, scoutSsh = sshInfo()
    cmdTemplate = env.get_template("scout_reboot_ap")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Running scout --reboot on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

