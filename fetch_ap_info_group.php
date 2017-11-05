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

// Cardinal Login Session

session_start();

// If user is not logged into Cardinal, then redirect them to the login page

if (!isset($_SESSION['username'])) {
header('Location: index.php');
}

// MySQL connection information

require_once('includes/dbconnect.php');

// Fetch POST data from configure_aps.html and execute SQL queries
$varConfID = $_POST['id'];

$sql = "SELECT ap_snmp,ap_ip FROM access_points WHERE ap_group_id = '$varConfID'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // store data of each row
    while($row = $result->fetch_assoc()) {
       $querySNMP = $row["ap_snmp"];
       $queryIP = $row["ap_ip"];
       $fetchAPName = shell_exec("snmpget -v2c -c $querySNMP $queryIP iso.3.6.1.2.1.1.5.0");
       $fetchAPMac = shell_exec("snmpget -v2c -c $querySNMP $queryIP iso.3.6.1.2.1.2.2.1.6.3");
       $fetchAPModel = shell_exec("snmpget -v2c -c $querySNMP $queryIP iso.3.6.1.2.1.47.1.1.1.1.13.1");
       $fetchAPSerial = shell_exec("snmpget -v2c -c $querySNMP $queryIP iso.3.6.1.2.1.47.1.1.1.1.11.1");
       $fetchAPBuilding = shell_exec("snmpget -v2c -c $querySNMP $queryIP iso.3.6.1.2.1.1.6.0");
       $fetchAPIOS = shell_exec("snmpget -v2c -c $querySNMP $queryIP iso.3.6.1.2.1.1.1.0");
	
       echo "<font face=\"Verdana\">\n";
       echo "Your Access Point Name is: $fetchAPName";
       echo "<br>";
       echo "</br>";
       echo "Your Access Point MAC Address is: $fetchAPMac";
       echo "<br>";
       echo "</br>";
       echo "Your Access Point Model is: $fetchAPModel";
       echo "<br>";
       echo "</br>";
       echo "Your Access Point Serial Number is: $fetchAPSerial";
       echo "<br>";
       echo "</br>";
       echo "Your Access Point Building Location is: $fetchAPBuilding";
       echo "<br>";
       echo "</br>";
       echo "Your Access Point IOS Version is: $fetchAPIOS";
       echo "<br>";
       echo "</br>";
     }
} else {
    echo "";
}

// Link back to the configure_access_point_groups.php
echo "<a href=\"configure_access_point_groups.php\">Back to Configure AP Groups Menu</a>";
echo "</font>";

$conn->close();

?>

