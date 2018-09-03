Delete Access Point Groups
##########################
:date: 2017-10-29 13:10
:author: Falcon
:slug: delete-access-point-groups

|image0|

The Cardinal **Delete Access Point Groups** tile is where an user can
delete an AP group from Cardinal.

|image1|

All this feature does is delete the AP group from the Cardinal database.
I am currently still working on a management interface for AP
configurations via the database. I plan to have some type of GUI where
the user can change AP settings, on the fly. These settings include AP
group memberships, SSID associations, etc. For now, if you wish to
delete an access point group, please make sure that you update the
database entries to the correct group id. If this is not performed, then
SSH actions will not work.

.. |image0| image:: http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f7e9300c0f6.png
.. |image1| image:: http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/10/img_59f7e9667fab7.png
