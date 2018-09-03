Installation
############
:date: 2017-07-07 22:40
:author: Falcon
:slug: installation

After you have chosen an appropriate Linux distro and installed the
software dependencies, we can begin the installation of Cardinal.

Run a Git Clone
~~~~~~~~~~~~~~~

1.) Navigate to the web-enabled directory you wish to install Cardinal
in. Once you are there, run a git clone:

.. code:: EnlighterJSRAW

    git clone https://github.com/falcon78921/Cardinal.git

You can also download the project as a .ZIP archive and then extract the
project in the desired directory:

.. code:: EnlighterJSRAW

    wget https://github.com/falcon78921/Cardinal/archive/master.zip
    cp master.zip /path/to/your/directory
    cd /path/to/your/directory
    unzip master.zip

Running the Install Script
~~~~~~~~~~~~~~~~~~~~~~~~~~

1.) Once you have fetched the Cardinal project, navigate to the
install.sh script. The install.sh script is located in
**$cardinal\_base/scripts/install. **

2.) Now, in order to configure Cardinal initially, please run the script
as **root**. Running this script will **NOT** do anything detrimental.
The only thing that might be wiped is the crontab, which will be
re-created with a fetch\_all\_clients.php entry (for querying connected
clients). For more information about the script, please refer below:

**IMPORTANT:** Anytime you run the install.sh script, please wipe out
the fetch\_all\_clients.php crontab job. Also delete the
php\_cardinal.ini and cardinal\_config.ini files. The install.sh script
will generate fresh entries based on your updated inputs.

Data That The Install.sh Script Will Ask For
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.) IP/Hostname of MySQL Server (default is typically
127.0.0.1/localhost)

2.) MySQL Database User

3.) MySQL Database Password

4.) Desired Database Name (for Cardinal System)

5.) Cardinal Dashboard Admin Username

6.) Cardinal Dashboard Admin Password

7.) Directory for Storing MySQL Connection Information

-  *It's recommended that you store this file outside of the web root.
   However, please ensure that this file is still readable by the web
   root. The install.sh script will take care of this. *

8.) Directory for Storing Cardinal Configuration Information

-  *It's recommended that you store this file outside of the web root.
   However, please ensure that this file is still readable by the web
   root. The install.sh script will take care of this. *

9.) Directory for Storing Cardinal Python Scripts

-  *It's recommended that you store this directory outside of the web
   root. However, please ensure that this directory is still readable by
   the web root. The install.sh script will take care of this. I would
   recommend creating a dedicated directory for these scripts. Once you
   have created a dedicated directory, copy all of the contents in the
   **scripts** directory into this directory. *

10.) Directory Where Cardinal Is Located

-  *This is typically /var/www or wherever your Apache2 web root is. *

If you wish to analyze the install.sh script, please check it out on
Cardinal's GitHub Repo.

**Set Cardinal Configuration Paths**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is something I definitely want to improve on, in the future. For
now, you have to update some Cardinal resources manually.

1.) Navigate to the **includes** directory, and edit the **$config**
variable in the \ **cardinalconfig.php** file to match the appropriate
location:

.. code:: EnlighterJSRAW

    <?php

    // Load configuration as an array. Use the actual location of your configuration file
       $config = parse_ini_file('/path/to/cardinal_config.ini'); 
       $scriptsDir = $config['scriptsdir']

    ?>

2.) Navigate to the **includes** directory, and edit the **$config**
variable in the \ **dbconnect.php** file to match the appropriate
location:

.. code:: EnlighterJSRAW

    <?php

    function db_connect() {

            // Define connection as a static variable, to avoid connecting more than once 
        static $conn;

            // Try and connect to the database, if a connection has not been established yet
        if(!isset($conn)) {
                 // Load configuration as an array. Use the actual location of your configuration file
            $config = parse_ini_file('/path/to/php_cardinal.ini'); // CHANGE THIS TO THE APPROPRIATE LOCATION!
            $conn = mysqli_connect($config['servername'],$config['username'],$config['password'],$config['dbname']);
        }

            // If connection was not successful, handle the error
        if($conn === false) {
                // Handle error - notify administrator, log to a file, show an error screen, etc.
            return mysqli_connect_error(); 
        }
        return $conn;
    }

    // Connect to the database
    $conn = db_connect();

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    ?>

3.) Navigate to where your **scripts** directory is located, and then
modify the following files:

**create\_building\_map.sh** - Modify the **cardinalBase** variable and
input the location of **cardinal\_config.ini**

.. code:: EnlighterJSRAW

    #!/bin/bash

    # Create Cardinal Heatmap
    # falcon78921

    # Cardinal Configuration Variable Declarations

    cardinalBase=$(awk -F "=" '/cardinalbase/ {print $2}' /path/to/cardinal_config.ini)

    # First, we generate the file from given information in add_new_heatmap.php

    cat $cardinalBase/assets/templates/building_template.php > $cardinalBase/assets/building_maps/.php
    mv $cardinalBase/assets/building_maps/.php $cardinalBase/assets/building_maps/$1.php

    # Now, we need to modify file per variables

    sed -i 's/$locationName/'$1'/g' $cardinalBase/assets/building_maps/$1.php
    sed -i 's/$heatmapImage/'$2'/g' $cardinalBase/assets/building_maps/$1.php

**create\_heatmap\_ap.sh** - Modify the **cardinalBase** variable and
input the location of **cardinal\_config.ini**

.. code:: EnlighterJSRAW

    #!/bin/bash

    # Create Cardinal Heatmap AP
    # falcon78921

    # Cardinal Configuration Variable Declarations

    # IMPORTANT!: Modify this to include the proper location of cardinal_config.ini
    cardinalBase=$(awk -F "=" '/cardinalbase/ {print $2}' /path/to/cardinal_config.ini)

    # Append the information sent from the add_new_ap_heatmap.php page to the following heatmap page
    # Start from reverse, each access point will go below the Cardinal APS GO BELOW HERE comment 

    sed -i '/Cardinal APS GO BELOW HERE/aecho "\n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "heatmapInstance.addData('"$1"');\n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "};\n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "  value: '"$7"' // the value at datapoint(x, y)\n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "  y: '"$6"', // y coordinate of the datapoint, a number\n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "  x: '"$5"', // x coordinate of the datapoint, a number \n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "  max: '"$4"', \n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "  min: '"$3"',\n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "var '"$1"' = {\n";' $cardinalBase/assets/building_maps/$2
    sed -i '/Cardinal APS GO BELOW HERE/aecho "// '"$1"' datapoint\n";' $cardinalBase/assets/building_maps/$2

**fetch\_total\_clients.sh** - Modify the **scriptsDir** variable and
input the location of **cardinal\_config.ini**

.. code:: EnlighterJSRAW

    #!/bin/bash

    # Cardinal Fetch Total Number of Clients Associated
    # falcon78921

    # After we have queried the SQL database, launched the associations command
    # via SSH, and received the output.

    # Cardinal Configuration Variable Declarations

    # IMPORTANT!: Modify this to include the proper location of the scripts directory
    scriptsDir=$(awk -F "=" '/scriptsdir/ {print $2}' /path/to/cardinal_config.ini)

    # Open Connection to Each AP in Cardinal Database

    python $scriptsDir/cisco_count_clients.py $1 $2 $3 $4 > $scriptsDir/results/$4.results

    # Run grep query, specifically for MAC addresses that were collected from PHP script

    grep -o "[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f].[0-9,a-f][0-9,a-f][0-9,a-f][0-9,a-f]" $scriptsDir/results/$4.results > $scriptsDir/results/$4.macs.txt

    # Run line count to get exact amount of clients associated, for each access point. Remove excess files.

    rm -r $scriptsDir/results/*.results
    wc -l < $scriptsDir/results/$4.macs.txt > $scriptsDir/results/$4.clients

    # Remove excess files. There you go!

    rm -r $scriptsDir/results/*.macs.txt

    # Rinse & Repeat!

**fetch\_all\_clients.php** - Modify the **Cardinal Configuration
Information** and **MySQL Connection Information **\ to the proper
locations (*dbconnect.php* and *cardinalconfig.php*)

.. code:: EnlighterJSRAW

    <?php
    /* Cardinal - An Open Source Cisco Wireless Access Point Controller
    MIT License
    Copyright © 2017 falcon78921
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    */
    // Cardinal Configuration Information
    require_once('/path/to/includes/cardinalconfig.php');
    // MySQL connection information
    require_once('/path/to/includes/dbconnect.php');
    // Run Cisco Client Command & Store Results in SQL
    $sql = "SELECT ap_ip,ap_ssh_username,ap_ssh_password,ap_name,ap_id FROM access_points WHERE ap_all_id = 2";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        // store data of each row
        while($row = $result->fetch_assoc()) {
           $queryIP = $row["ap_ip"];
           $queryUser = $row["ap_ssh_username"];
           $queryPass = $row["ap_ssh_password"];
           $queryName = $row["ap_name"];
           $queryID = $row["ap_id"];
           $bashCommand = escapeshellcmd("$scriptsDir/fetch_total_clients.sh $queryIP $queryUser $queryPass $queryName");
           $bashOutput = shell_exec($bashCommand);
           $bashClients = escapeshellcmd("cat $scriptsDir/results/$queryName.clients");
           $bashClientsOutput = shell_exec($bashClients);
           $bashWipeClients = escapeshellcmd("rm $scriptsDir/results/$queryName.clients");
           $bashWipeClientsExec = shell_exec($bashWipeClients);
           $phpMySQLUpdate = "UPDATE access_points SET ap_total_clients = '$bashClientsOutput' WHERE ap_id = $queryID";
           $phpMySQLQuery = mysqli_query($conn,$phpMySQLUpdate);
           $phpMySQLValue = mysqli_fetch_object($phpMySQLQuery);
         }
    } else {
        echo "";
    }
    $conn->close();
    ?>

**Clean Up! **
~~~~~~~~~~~~~~

Once the **scripts** directory is copied into the desired location, you
can delete the old scripts directory out of the Cardinal root. You can
also delete the **sql** directory as well.

**IMPORTANT:** I would recommend backing up the **cardinal.sql** schema,
just in case something happens with your system and needs recovered.

You can also download the **cardinal.sql** schema off of Cardinal's
GitHub repo.

**Finished! **
~~~~~~~~~~~~~~

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
