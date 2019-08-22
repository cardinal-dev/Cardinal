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

import scout_info_commands
import scout_sys_commands
import scout_ssid_commands
import sys

# CARDINAL SETTINGS

scoutCommand = sys.argv[1]

# SCOUT HELP & USAGE

if scoutCommand == "--help":
    print("Scout: Cardinal CLI for managing Cisco access points")
    print("Usage:")
    print("   scout.py --get-arp: print access point ARP table")
    print("   scout.py --led: trigger LED function for 30 seconds")
    print("   scout.py --change-ip: change access point IP")
    print("   scout.py --create-ssid-24: create a 2.4GHz SSID")
    print("   scout.py --create-ssid-5: create a 5GHz SSID")
    print("   scout.py --create-ssid-radius-24: create a 2.4GHz RADIUS SSID")
    print("   scout.py --create-ssid-radius-5: create a 5GHz RADIUS SSID")
    print("   scout.py --delete-ssid-24: delete a 2.4GHz SSID")
    print("   scout.py --delete-ssid-5: delete a 5GHz SSID")
    print("   scout.py --delete-ssid-radius-24: delete a 2.4GHz RADIUS SSID")
    print("   scout.py --delete-ssid-radius-5: delete a 5GHz RADIUS SSID")
    print("   scout.py --disable-http: disable access point HTTP server")
    print("   scout.py --disable-radius: disable access point RADIUS function") 
    print("   scout.py --disable-snmp: disable access point SNMP function")
    print("   scout.py --enable-http: enable access point HTTP function")
    print("   scout.py --enable-radius: enable access point RADIUS function")
    print("   scout.py --enable-snmp: enable access point SNMP function")
    print("   scout.py --get-speed: show access point link speed")
    print("   scout.py --tftp-backup: backup access point config via TFTP")
    print("   scout.py --wr: write configuration to access point")
    print("   scout.py --erase: erase configuration on access point")
    print("   scout.py --count-clients: fetch client associations on access point")
    print("   scout.py --get-name: fetch access point hostname")
    print("   scout.py --get-users: fetch access point users")
    print("   scout.py --get-mac: fetch access point MAC address")
    print("   scout.py --get-model: fetch access point model info")
    print("   scout.py --get-serial: fetch access point serial number")
    print("   scout.py --get-location: fetch access point location")
    print("   scout.py --get-ios-info: fetch access point IOS info")
    print("   scout.py --get-uptime: fetch access point uptime info")
    print("   scout.py --reboot: reboot access point")
    print("   scout.py --change-name: change access point hostname")

# Scout Info Commands

if scoutCommand == "--get-arp":
    scout_info_commands.scoutGetArp()

if scoutCommand == "--get-speed":
    scout_info_commands.scoutGetSpeed()

if scoutCommand == "--count-clients":
    scout_info_commands.scoutCountClients()

if scoutCommand == "--get-mac":
    scout_info_commands.scoutGetMac()

if scoutCommand == "--get-model":
    scout_info_commands.scoutGetModel()

if scoutCommand == "--get-name":
    scout_info_commands.scoutGetHostname()

if scoutCommand == "--get-serial":
    scout_info_commands.scoutGetSerial()

if scoutCommand == "--get-ios-info":
    scout_info_commands.scoutGetIosInfo()

if scoutCommand == "--get-location":
    scout_info_commands.scoutGetLocation()

if scoutCommand == "--get-uptime":
    scout_info_commands.scoutGetUptime()

if scoutCommand == "--get-users":
    scout_info_commands.scoutGetUsers()

# Scout Sys Commands

if scoutCommand == "--led":
    scout_sys_commands.scoutLed()

if scoutCommand == "--change-ip":
    scout_sys_commands.scoutChangeIp()

if scoutCommand == "--disable-http":
    scout_sys_commands.scoutDisableHttp()

if scoutCommand == "--disable-radius":
    scout_sys_commands.scoutDisableRadius()

if scoutCommand == "--disable-snmp":
    scout_sys_commands.scoutDisableSnmp()

if scoutCommand == "--enable-http":
    scout_sys_commands.scoutEnableHttp()

if scoutCommand == "--enable-radius":
    scout_sys_commands.scoutEnableRadius()

if scoutCommand == "--enable-snmp":
    scout_sys_commands.scoutEnableSnmp()

if scoutCommand == "--tftp-backup":
    scout_sys_commands.scoutTftpBackup()

if scoutCommand == "--wr":
    scout_sys_commands.scoutDoWr()

if scoutCommand == "--erase":
    scout_sys_commands.scoutWriteDefault()

if scoutCommand == "--reboot":
    scout_sys_commands.scoutDoReboot()

if scoutCommand == "--change-name":
    scout_sys_commands.scoutChangeName()

# Scout Ssid Commands

if scoutCommand == "--create-ssid-24":
    scout_ssid_commands.scoutCreateSsid24()

if scoutCommand == "--create-ssid-5":
    scout_ssid_commands.scoutCreateSsid5()

if scoutCommand == "--create-ssid-radius-24":
    scout_ssid_commands.scoutCreateSsid24Radius()

if scoutCommand == "--create-ssid-radius-5":
    scout_ssid_commands.scoutCreateSsidRadius5()

if (scoutCommand == "--delete-ssid-24") or (scoutCommand == "--delete-ssid-radius-24"):
    scout_ssid_commands.scoutDeleteSsid24()

if (scoutCommand == "--delete-ssid-5") or (scoutCommand == "--delete-ssid-radius-5"):
    scout_ssid_commands.scoutDeleteSsid5()
