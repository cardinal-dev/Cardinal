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

# SCOUT SYS COMMAND FUNCTIONS

def scoutLed(ip, username, password):
    """Function that opens a SSH connection to the AP
    and runs led flash 30.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    print("INFO: Flashing pretty lights on {}...".format(ip))
    stdin, stdout, stderr = scoutSsh.exec_command("led flash 30\n")
    scoutSsh.close()

def scoutChangeIp(ip, username, password, newIp, subnetMask):
    """Function that identifies SSH info, collects sys args,
    calls the scout_change_ap_ip command set, opens a SSH connection
    to the AP, executes the IP change, terminates the old SSH connection,
    opens a new one, and runs the scout_do_wr command set to save new IP
    change.
    """
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    newIp = newIp
    subnetMask = subnetMask
    cmdTemplate = env.get_template("scout_change_ap_ip")
    cmds = cmdTemplate.render(password=password,newIp=newIp,subnetMask=subnetMask)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Changing IP from {0} to {1}...".format(ip,newIp))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()
    scoutDoWr(ip=newIp, username=username, password=password)

def scoutDisableHttp(ip, username, password):
    """Function that disables the HTTP server on AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_disable_ap_http")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Disabling HTTP server on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDisableRadius(ip, username, password):
    """Function that disables RADIUS on AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_disable_ap_radius")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Disabling RADIUS on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDisableSnmp(ip, username, password):
    """Function that disables SNMP on AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_disable_ap_snmp")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Disabling SNMP server on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutEnableHttp(ip, username, password):
    """Function that enables the HTTP server on AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_enable_ap_http")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Enabling HTTP server on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutEnableRadius(ip, username, password):
    """Function that enables RADIUS on AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_enable_ap_radius")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Enabling RADIUS on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutEnableSnmp(ip, username, password, snmp):
    """Function that enables SNMP on AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    snmp = snmp
    cmdTemplate = env.get_template("scout_enable_ap_snmp")
    cmds = cmdTemplate.render(password=password,snmp=snmp)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Enabling SNMP server on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutTftpBackup(ip, username, password, tftpIp):
    """Function that performs TFTP backup of AP config."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    tftpIp = tftpIp
    cmdTemplate = env.get_template("scout_do_tftp_backup")
    cmds = cmdTemplate.render(password=password,tftpIp=tftpIp)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Generating TFTP backup for {0} and sending to {1}...".format(ip,tftpIp))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDoWr(ip, username, password):
    """Function that performs write command on AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_do_wr")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Committing changes on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutWriteDefault(ip, username, password):
    """Function that wipes AP memory back to default."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_write_default")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Erasing config on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutChangeName(ip, username, password, apName):
    """Function that changes the hostname of AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    apName = apName
    cmdTemplate = env.get_template("scout_change_ap_name")
    cmds = cmdTemplate.render(apName=apName,password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Changing AP hostname on {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()

def scoutDoReboot(ip, username, password):
    """Function that reboots AP."""
    scoutSsh = scout_auth.sshInfo(ip=ip, username=username, password=password)
    env = scout_env.scoutEnv()
    cmdTemplate = env.get_template("scout_reboot_ap")
    cmds = cmdTemplate.render(password=password)
    scoutCommands = cmds.splitlines()
    channel = scoutSsh.invoke_shell()
    print("INFO: Rebooting {}...".format(ip))
    for command in scoutCommands:
        channel.send('{}\n'.format(command))
        time.sleep(.10)
    scoutSsh.close()
