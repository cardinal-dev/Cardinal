---
title: Configure SSIDs (2.4GHz)
---

![image0](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f61652e55c1.png)

The Cardinal **Configure SSIDs (2.4GHz)** tile is where an user can
configure a 2.4GHz SSID on a single access point.

![image1](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f6169d090e2.png)

**SSID Name** - This is the name of the WiFi network that will be
created, and users will connect to it.

**WPA2-PSK** - Cardinal does **NOT** support WEP. Cardinal only supports
WPA2-PSK passphrases. The passphrase requires a minimum of 8 characters.

**VLAN** - This is the VLAN that user data will be sent on. Please make
sure that you configure your switch ports as well. Access point
operations will not work correctly if a switch port is not
VLAN'd/trunked correctly.

**Bridge Group ID** - This is the bridge group ID that the 2.4GHz and
Ethernet interface will connect on.

**2.4GHz Radio Sub Interface ID** - This is the sub-interface that the
SSID will communicate on.

**Gigabit Sub Interface ID** - This is the sub-interface created for
client data communications, per SSID/VLAN.

If you wish to configure multiple access points with the same SSID,
please use the **Configure SSID 2.4GHz (Group)** tile. Please make sure
you create an access point group before utilizing this feature.