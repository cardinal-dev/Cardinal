Configure SSIDs (5GHz)
######################
:date: 2017-10-29 13:10
:author: Falcon
:slug: configure-ssids-5ghz

|image0|

The Cardinal \ **Configure SSIDs (5GHz)** tile is where an user can
configure a 5GHz SSID on a single access point.

|image1|

**SSID Name** – This is the name of the WiFi network that will be
created, and users will connect to it.

**WPA2-PSK** – Cardinal does \ **NOT** support WEP. Cardinal only
supports WPA2-PSK passphrases. The passphrase requires a minimum of 8
characters.

**VLAN** – This is the VLAN that user data will be sent on. Please make
sure that you configure your switch ports as well. Access point
operations will not work correctly if a switch port is not
VLAN’d/trunked correctly.

**Bridge Group ID** – This is the bridge group ID that the 5GHz and
Ethernet interface will connect on.

**5GHz Radio Sub Interface ID** – This is the sub-interface that the
SSID will communicate on.

**Gigabit Sub Interface ID** – This is the sub-interface created for
client data communications, per SSID/VLAN.

If you wish to configure multiple access points with the same SSID,
please use the \ **Configure SSID 5GHz (Group)** tile. Please make sure
you create an access point group before utilizing this feature.

.. |image0| image:: http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f7e1e401ae5.png
.. |image1| image:: http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f7e1a09ee2a.png
