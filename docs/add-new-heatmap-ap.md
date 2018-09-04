Add New Heatmap AP
==================

date
:   2017-09-28 20:49

author
:   Falcon

slug
:   add-new-heatmap-ap

![image0](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/09/img_59cd98c2c2a6d.png)

The **Add New Heatmap AP** tile is where you can add an access point to
a heatmap.

***IMPORTANT: The heatmap functionality in Cardinal is still
in-development! Complete accuracy is not guaranteed and only should be
used for estimated coverage! ***

When you click on the map icon, a modal will appear. The modal will look
like this:

![image1](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/09/img_59cd993fae3e6.png)

**AP Name** - This is where you input the name of the access point for
heatmap display. For example, you can call this access point
*AP\_RM\_301*.

**Choose Heatmap** - This is where you select which heatmap the access
point will go on. This option will display a drop down of all the PHP
pages in the ***\$cardinal\_base/assets/building\_maps*** directory.

**Data Minimum** - This is where you specify the minimum data (in dB).
Typically, I would imagine the minimum dB for an AP would be in the 30's
(great signal).

**Data Maximum** - This is where you specify the maximum data (in dB).
Typically, I would imagine the maximum dB for an AP would be in the 90's
(very noisy, bad signal).

**X-Coordinate Datapoint** - Currently, Cardinal doesn't have a dynamic
plotting mechanism for AP heatmaps. This could change, if anyone is
interested in helping out with this, please refer to my GitHub for the
latest issue data. In order to plot AP's on the heatmap, please use a
pixel ruler. I recommend using Page Ruler (Chrome Extension) to plot a
point on the AP heatmap. Then, take the values of Right for X and Top
for Y.

**Y-Coordinate Datapoint** - Currently, Cardinal doesn't have a dynamic
plotting mechanism for AP heatmaps. This could change, if anyone is
interested in helping out with this, please refer to my GitHub for the
latest issue data. In order to plot AP's on the heatmap, please use a
pixel ruler. I recommend using Page Ruler (Chrome Extension) to plot a
point on the AP heatmap. Then, take the values of Right for X and Top
for Y.

**Data Value (in dB)** - For now, I would perform a site survey and get
an approximate dB reading for the data value. In my environment, the dB
readings averaged between 60-70dB. So, if a client connected to my AP,
the dB noise was between 60-70dB, so I would put about 65dB in.
