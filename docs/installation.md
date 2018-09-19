Installation
============

After you have chosen an appropriate Linux distro and installed the
software dependencies, we can begin the installation of Cardinal.

Run a Git Clone
---------------

1.) Navigate to the web-enabled directory you wish to install Cardinal
in. Once you are there, run a git clone:

`git clone https://github.com/falcon78921/Cardinal.git`

You can also download the project as a .ZIP archive and then extract the
project in the desired directory:

`wget https://github.com/falcon78921/Cardinal/archive/master.zip` <br>
`cp master.zip /path/to/your/directory` <br>
`cd /path/to/your/directory` <br>
`unzip master.zip`

Running the Install Script
--------------------------

1.) Once you have fetched the Cardinal project, navigate to the
install.sh script. The install.sh script is located in
**\$cardinal\_base/scripts/install. **

2.) Now, in order to configure Cardinal initially, please run the script
as **root**. Running this script will **NOT** do anything detrimental.
The only thing that might be wiped is the crontab, which will be
re-created with a fetch\_all\_clients.php entry (for querying connected
clients). For more information about the script, please refer below:

**IMPORTANT:** Anytime you run the install.sh script, please wipe out
the fetch\_all\_clients.php crontab job. Also delete the
php\_cardinal.ini and cardinal\_config.ini files. The install.sh script
will generate fresh entries based on your updated inputs.

### Desired Data

1.) IP/Hostname of MySQL Server (default is typically
127.0.0.1/localhost)

2.) MySQL Database User

3.) MySQL Database Password

4.) Desired Database Name (for Cardinal System)

5.) Cardinal Dashboard Admin Username

6.) Cardinal Dashboard Admin Password

7.) Directory for Storing MySQL Connection Information

-   *It's recommended that you store this file outside of the web root.
    However, please ensure that this file is still readable by the web
    root. The install.sh script will take care of this. *

8.) Directory for Storing Cardinal Configuration Information

-   *It's recommended that you store this file outside of the web root.
    However, please ensure that this file is still readable by the web
    root. The install.sh script will take care of this. *

9.) Directory for Storing Cardinal Python Scripts

-   *It's recommended that you store this directory outside of the web
    root. However, please ensure that this directory is still readable
    by the web root. The install.sh script will take care of this. I
    would recommend creating a dedicated directory for these scripts.
    Once you have created a dedicated directory, copy all of the
    contents in the `scripts` directory into this directory.*

10.) Directory Where Cardinal Is Located

-   *This is typically /var/www or wherever your Apache2 web root is. *

If you wish to analyze the install.sh script, please check it out on
Cardinal's GitHub Repo.

**Clean Up! **
--------------

Once the **scripts** directory is copied into the desired location, you
can delete the old scripts directory out of the Cardinal root. You can
also delete the **sql** directory as well.

**IMPORTANT:** I would recommend backing up the **cardinal.sql** schema,
just in case something happens with your system and needs recovered.

You can also download the **cardinal.sql** schema off of Cardinal's
GitHub repo.

**Finished! **
--------------

Congratulations! By now, you should have a functional installation of
Cardinal. In order to start, please make sure your Cisco access points
are SSH-configured. Also, please make sure you assign static IP
addresses to the access points as well.

One way you can simplify adding access points via DHCP is by first
collecting the IP addresses of all access points. Then, add them as
access points into Cardinal. Now, use the **Change Access Point IP**
tile and set the desired IP address. Remember, this will statically set
the IP address for the access point and update the IP address in
Cardinal's database.

If I'm missing any directions, software dependencies, etc., please add
an Issue on Cardinal's GitHub repo and I'll look into it as soon as
possible. If you have any recommendations for improvement, whether it be
system operations or documentation, please post these improvements using
the Issue tab on Cardinal's GitHub repo.
