Software Dependencies
=====================

date
:   2017-07-07 22:40

author
:   Falcon

slug
:   software-dependencies

Once you have your OS in order, here are some important software
dependencies to install. Again, I used Ubuntu 14.04.2 LTS Server, so the
software used might have updated versions available. Please check your
current Linux distro and make sure your sources are in check.

**NOTE:** If I'm missing something, please let me know via the Issues
page on Cardinal's GitHub repo.

Here is what you need:

**Altogether now! **
--------------------

Before running Altogether now!, please add this Launchpad PPA (Ubuntu):

~~~~ {.sourceCode .EnlighterJSRAW}
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update
~~~~

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install openssh-server openssh-client mysql-server mysql-client git apache2 python-paramiko python php7.0 php7.0-mysql snmp nmap curl traceroute whois tftpd-hpa
~~~~

**Dependencies (One by One)**
-----------------------------

**OpenSSH Client/Server (For Cardinal SSH functionality/ease of use)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install openssh-server openssh-client
~~~~

**MySQL 5.5 Client/Server (For Cardinal backend functionality)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install mysql-server mysql-client
~~~~

**Git (To fetch Cardinal project from GitHub)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install git
~~~~

**Apache2 2.4 (To host Cardinal project on HTTP server)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install apache2
~~~~

**Python (For using Paramiko (Python-dependent) to establish SSH
connections between access points and Cardinal)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install python
~~~~

**Paramiko (For creating SSH connections via Python. This is to send
commands from Cardinal to access points)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install python-paramiko
~~~~

**PHP 7.0 (For web-based logic, particularly with the dashboard,
database (MySQL), etc.)**

~~~~ {.sourceCode .EnlighterJSRAW}
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update
sudo apt-get install php7.0
~~~~

**PHP 7.0 Module Dependencies**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install php7.0-mysql
~~~~

**Net-SNMP (For SNMP-based operations (e.g. Rebooting AP via SNMP,
fetching AP info, etc.))**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install snmp
~~~~

**Nmap (For port scanning & network information)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install nmap
~~~~

**cURL (For using cURL functionality via Network Toolkit)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install curl
~~~~

**Traceroute (For using the traceroute tool via Network Toolkit)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install traceroute
~~~~

**Whois (For looking up domain registrations via Network Toolkit)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install whois
~~~~

**tftpd-hpa (For hosting TFTP server on Cardinal system)**

~~~~ {.sourceCode .EnlighterJSRAW}
apt-get install tftpd-hpa
~~~~
