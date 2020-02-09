---
title: Cardinal Access Point Statistics
---

![image0](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/09/img_59c87c446e1d0.png)

The **Cardinal Access Point Statistics** menu is where users can see the
amount of AP's, clients associated to AP's, and amount of AP groups
within Cardinal. The graphs are generated using
***[chart.js](http://www.chartjs.org/).*** The data is stored within the
MySQL backend. For the **Total Number of Clients Associated**, please
make sure you have the crontab entry. The crontab entry for
*fetch\_all\_clients.php* is exceptionally important. For example,
within the *install.sh* script, you should see a portion that contains
this:

|
![image1](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/09/img_59c87c6dcbb5a.png)
| The preceding portion of Bash will add the following to your system's
crontab:

![image2](http://cardinal.mcclunetechnologies.net/wp-content/uploads/2017/09/img_59c87c845e1b3.png)

Now, the Cardinal base directory will differ depending on your system
and your preferences. However, this script will run every minute and
query the amount of clients associated to the access points. Depending
on the amount of access points within your installation of Cardinal, you
might want to increase the crontab interval. If you have many access
points in your system and you run *fetch\_all\_clients.php* every
minute, you might run into processing problems.