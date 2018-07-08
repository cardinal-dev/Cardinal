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

require_once('/var/www/html/includes/cardinalconfig.php');

// MySQL connection information

require_once('/var/www/html/includes/dbconnect.php');

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
