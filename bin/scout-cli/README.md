<h1>scout-cli</h1>
<h3>CLI for Managing Cisco Autonomous APs</h3>

`scout-cli` exposes `scout` logic in order to manage Cisco APs via the CLI. Instead of passing positional arguments
directly into the functions, `scout-cli` uses the `sys` module in order to gather the values needed to run.

<h3>Usage:</h3>

~~~
scout-cli: Cardinal CLI for Managing Cisco Access Points
Usage:
   scout-cli --get-arp: print access point ARP table
   scout-cli --led: trigger LED function for 30 seconds
   scout-cli --change-ip: change access point IP
   scout-cli --create-ssid-24: create a 2.4GHz SSID
   scout-cli --create-ssid-5: create a 5GHz SSID
   scout-cli --create-ssid-radius-24: create a 2.4GHz RADIUS SSID
   scout-cli --create-ssid-radius-5: create a 5GHz RADIUS SSID
   scout-cli --delete-ssid-24: delete a 2.4GHz SSID
   scout-cli --delete-ssid-5: delete a 5GHz SSID
   scout-cli --delete-ssid-radius-24: delete a 2.4GHz RADIUS SSID
   scout-cli --delete-ssid-radius-5: delete a 5GHz RADIUS SSID
   scout-cli --disable-http: disable access point HTTP server
   scout-cli --disable-radius: disable access point RADIUS function
   scout-cli --disable-snmp: disable access point SNMP function
   scout-cli --enable-http: enable access point HTTP function
   scout-cli --enable-radius: enable access point RADIUS function
   scout-cli --enable-snmp: enable access point SNMP function
   scout-cli --get-speed: show access point link speed
   scout-cli --tftp-backup: backup access point config via TFTP
   scout-cli --wr: write configuration to access point
   scout-cli --erase: erase configuration on access point
   scout-cli --count-clients: fetch client associations on access point
   scout-cli --get-name: fetch access point hostname
   scout-cli --get-users: fetch access point users
   scout-cli --get-mac: fetch access point MAC address
   scout-cli --get-model: fetch access point model info
   scout-cli --get-serial: fetch access point serial number
   scout-cli --get-location: fetch access point location
   scout-cli --get-ios-info: fetch access point IOS info
   scout-cli --get-uptime: fetch access point uptime info
   scout-cli --reboot: reboot access point
   scout-cli --change-name: change access point hostname
~~~

Just like `scout`, values for `ip`, `username`, and `password` are always required. These values are given after the
command argument.

<h3>Example</h3>

~~~
scout-cli --get-arp <CISCO_AP_IP> <USERNAME> <PASSWORD>
~~~

~~~
scout-cli --get-arp 192.168.2.100 cisco1 mysecretpass
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.2.1             0   ec1a.5986.2510  ARPA   BVI1
Internet  192.168.2.3             1   7ce9.d306.090c  ARPA   BVI1
Internet  192.168.2.9             -   f866.f292.a65d  ARPA   BVI1
~~~
