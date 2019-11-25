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

import sys
import scout_sys
import scout_info
import scout_ssid

# SCOUT USAGE

def scoutUsage():
    print("scout-cli: Cardinal CLI for Managing Cisco Access Points")
    print("Usage:")
    print("   scout-cli --get-arp: print access point ARP table")
    print("   scout-cli --led: trigger LED function for 30 seconds")
    print("   scout-cli --change-ip: change access point IP")
    print("   scout-cli --create-ssid-24: create a 2.4GHz SSID")
    print("   scout-cli --create-ssid-5: create a 5GHz SSID")
    print("   scout-cli --create-ssid-radius-24: create a 2.4GHz RADIUS SSID")
    print("   scout-cli --create-ssid-radius-5: create a 5GHz RADIUS SSID")
    print("   scout-cli --delete-ssid-24: delete a 2.4GHz SSID")
    print("   scout-cli --delete-ssid-5: delete a 5GHz SSID")
    print("   scout-cli --delete-ssid-radius-24: delete a 2.4GHz RADIUS SSID")
    print("   scout-cli --delete-ssid-radius-5: delete a 5GHz RADIUS SSID") 
    print("   scout-cli --disable-http: disable access point HTTP server")
    print("   scout-cli --disable-radius: disable access point RADIUS function") 
    print("   scout-cli --disable-snmp: disable access point SNMP function")
    print("   scout-cli --enable-http: enable access point HTTP function")
    print("   scout-cli --enable-radius: enable access point RADIUS function")
    print("   scout-cli --enable-snmp: enable access point SNMP function")
    print("   scout-cli --get-speed: show access point link speed")
    print("   scout-cli --tftp-backup: backup access point config via TFTP")
    print("   scout-cli --wr: write configuration to access point")
    print("   scout-cli --erase: erase configuration on access point")
    print("   scout-cli --count-clients: fetch client associations on access point")
    print("   scout-cli --get-name: fetch access point hostname")
    print("   scout-cli --get-users: fetch access point users")
    print("   scout-cli --get-mac: fetch access point MAC address")
    print("   scout-cli --get-model: fetch access point model info")
    print("   scout-cli --get-serial: fetch access point serial number")
    print("   scout-cli --get-location: fetch access point location")
    print("   scout-cli --get-ios-info: fetch access point IOS info")
    print("   scout-cli --get-uptime: fetch access point uptime info")
    print("   scout-cli --reboot: reboot access point")
    print("   scout-cli --change-name: change access point hostname")

# SCOUT LOGIC

if len(sys.argv) > 1:
    scoutCommand = sys.argv[1]

    # SCOUT INFO COMMANDS
    if scoutCommand == "--help":
        scoutUsage()
    elif scoutCommand == "--get-arp":
        scout_info.scoutGetArp()
    elif scoutCommand == "--get-speed":
        scout_info.scoutGetSpeed()
    elif scoutCommand == "--count-clients":
        scout_info.scoutCountClients()
    elif scoutCommand == "--get-mac":
        scout_info.scoutGetMac()
    elif scoutCommand == "--get-model":
        scout_info.scoutGetModel()
    elif scoutCommand == "--get-name":
        scout_info.scoutGetHostname()
    elif scoutCommand == "--get-serial":
        scout_info.scoutGetSerial()
    elif scoutCommand == "--get-ios-info":
        scout_info.scoutGetIosInfo()
    elif scoutCommand == "--get-location":
        scout_info.scoutGetLocation()
    elif scoutCommand == "--get-uptime":
        scout_info.scoutGetUptime()
    elif scoutCommand == "--get-users":
        scout_info.scoutGetUsers()

    # SCOUT SYS COMMANDS
    if scoutCommand == "--led":
        scout_sys.scoutLed()
    elif scoutCommand == "--change-ip":
        scout_sys.scoutChangeIp()
    elif scoutCommand == "--disable-http":
        scout_sys.scoutDisableHttp()
    elif scoutCommand == "--disable-radius":
        scout_sys.scoutDisableRadius()
    elif scoutCommand == "--disable-snmp":
        scout_sys.scoutDisableSnmp()
    elif scoutCommand == "--enable-http":
        scout_sys.scoutEnableHttp()
    elif scoutCommand == "--enable-radius":
        scout_sys.scoutEnableRadius()
    elif scoutCommand == "--enable-snmp":
        scout_sys.scoutEnableSnmp()
    elif scoutCommand == "--tftp-backup":
        scout_sys.scoutTftpBackup()
    elif scoutCommand == "--wr":
        scout_sys.scoutDoWr()
    elif scoutCommand == "--erase":
        scout_sys.scoutWriteDefault()
    elif scoutCommand == "--reboot":
        scout_sys.scoutDoReboot()
    elif scoutCommand == "--change-name":
        scout_sys.scoutChangeName()

    # SCOUT SSID COMMANDS
    if scoutCommand == "--create-ssid-24":
        scout_ssid.scoutCreateSsid24()
    elif scoutCommand == "--create-ssid-5":
        scout_ssid.scoutCreateSsid5()
    elif scoutCommand == "--create-ssid-radius-24":
        scout_ssid.scoutCreateSsid24Radius()
    elif scoutCommand == "--create-ssid-radius-5":
        scout_ssid.scoutCreateSsidRadius5()
    elif (scoutCommand == "--delete-ssid-24") or (scoutCommand == "--delete-ssid-radius-24"):
        scout_ssid.scoutDeleteSsid24()
    elif (scoutCommand == "--delete-ssid-5") or (scoutCommand == "--delete-ssid-radius-5"):
        scout_ssid.scoutDeleteSsid5()

else:
    print("ERROR: No valid options detected. Please use --help for a list of valid options.")
