Configure RADIUS SSID (5GHz)
============================

date
:   2017-10-29 13:10

author
:   Falcon

slug
:   configure-radius-ssid-5ghz

![image0](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f7e8179c6d4.png)

The Cardinal **Configure RADIUS SSID (5GHz)** tile is where an user can
configure a 5GHz RADIUS SSID on a single access point.

![image1](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f7e7d3c404a.png)

**SSID Name** – This is the name of the WiFi network that will be
created, and users will connect to it.

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

**RADIUS Server** - This is the IP address/hostname of the RADIUS server
being used. Please make sure, whichever RADIUS server you use, to add
each AP as a NAS client.

**Shared Secret** - This is the shared secret between the AP and the
RADIUS server. Please make sure both secrets match.

**Authorization Port** - This is the RADIUS Auth port. Typically, the
port is **1812/UDP**. However, this depends on your RADIUS server
configuration.

**Accounting Port** - This is the RADIUS Acct port. Typically, the port
is **1813/UDP**. However, this depends on your RADIUS server
configuration.

**RADIUS Server Timeout (in seconds)** - The amount of time before the
RADIUS connection (between AP and server) times out.

**RADIUS Group** - The RADIUS group is used for grouping existing server
hosts for authentication. This can be a name that distinguishes that
group of servers.

**Method List** - Method Lists can be used to assign a list of methods
for Authentication, Authorization, and Accounting of RADIUS clients.
This can be a name that distinguishes that group of methods.

If you wish to configure multiple access points with the same SSID,
please use the **Configure RADIUS SSID 5GHz (Group)** tile. Please make
sure you create an access point group before utilizing this feature.
