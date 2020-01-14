<h1>scout</h1>
<h3>Managing Cisco Autonomous APs</h3>

`scout` is the underlying logic that communicates with Cisco Autonomous APs via SSH. The main driving force
is `paramiko`. `scout` is built on and requires Python3. `scout` and all of Cardinal components are tested
against Python 3.5, 3.6, and 3.7.

<h3>Example Usage:</h3>

~~~
Python 3.5.2 (default, Jul 10 2019, 11:58:48) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from scout import scout_info
>>> scout_info.scoutGetArp("192.168.2.5", "Cisco", "Cisco")
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.2.3            90   7ce9.d306.090c  ARPA   BVI1
Internet  192.168.2.5             -   442b.03a9.70d5  ARPA   BVI1
~~~

`scout` is a Python package that contains five modules:

`scout_auth` builds the `paramiko` client based on information passed into `sshInfo()`. `sshInfo()` accepts
three positional arguments: `ip`, `username`, and `password`.

`scout_env` contains the Jinja2 logic for building/running scout templates. Currently, all default scout templates can
be found in `bin/scout/templates`. Much like playbooks in Ansible, scout can read a text file that has
one Cisco command sequence per line. If desired, the user can pass Jinja2 values to the templates in order to build
complex command runs for automation. 

`scout_info` contains command functions that gather Cisco AP information, much like the commands a sysadmin
would type at the Terminal.

`scout_sys` contains command functions that manipulate certain system settings.

`scout_ssid` contains command functions that create/delete SSIDs on Cisco APs.

This isn't intending to replace Ansible at all (scout isn't even on the same level). scout is just a very simplified way of automating some of the 
management that comes with Cisco Autonomous APs.
