Configure Access Points (Group)
###############################
:date: 2017-10-29 13:08
:author: Falcon
:slug: configure-access-points-group

|image0|

The Cardinal **Configure Access Points (Group)** tile is where an user
can perform actions similar to the Configure Access Point tile, but to a
whole access point group. Currently, I am still working on the group
functions.

|image1|

The functions are the same as the Configure Access Point tile, except
the actions are applied to an entire AP group. Again, here are those
functions:

**Ping** - An user can ping the access point, to check connectivity from
Cardinal.

**Fetch Uptime** - An user can request the system uptime for a specific
access point. A reminder, in order for an user to utilize this feature,
SNMP must be enabled on the access point. To learn more about the SNMP
feature, please visit the **Configure SNMP** documentation.

**Reboot** - An user can execute a reboot on a specific access point.

**Fetch Info** - An user can request system information about the access
point. Information includes access point name, access point MAC address,
access point model, access point serial number, access point building
location, and access point IOS version. A reminder, in order for an user
to utilize this feature, SNMP must be enabled on the access point. To
learn more about the SNMP feature, please visit the **Configure SNMP**
documentation.

**Fetch ARP Table** - An user can request the ARP table for a specific
access point.

**Find Me!** - An user can request a 30 second LED blinking action, in
order to identify a certain access point.

**Flash AP** - An user can request an access point system wipe.
***IMPORTANT: Use this feature cautiously! This will wipe the access
point system NVRAM, and take the configuration back to factory
default.***

**Save AP Changes** - An user can request a simple "wr" command to a
specific access point.

 

.. |image0| image:: http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f610e7733ce.png
.. |image1| image:: http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f7e08a534d0.png
