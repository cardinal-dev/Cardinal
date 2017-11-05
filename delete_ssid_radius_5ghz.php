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

// Cardinal Configuration Information

require_once('includes/cardinalconfig.php');

// MySQL connection information

require_once('includes/dbconnect.php');

// HTML Dropdown for AP

$apDropdownQuery = $conn->query("SELECT ap_id,ap_name FROM access_points");

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font face=\"Verdana\">\n"; 
echo "Choose AP:";
echo "</font>";
echo "<form id=\"configure_ap\" action=\"\" method=\"POST\">\n";
echo "<select name='apid'>";

    while ($apRow = $apDropdownQuery->fetch_assoc()) {

                  unset($apId, $apName);
                  $apId = $apRow['ap_id'];
                  $apName = $apRow['ap_name'];
                  echo '<option value="'.$apId.'">'.$apName.'</option>';

}

echo "</select>";
echo "<br>";
echo "</br>";

// Dropdown for SSID Deletion

$ssidDropdownQuery = $conn->query("SELECT ap_ssid_id,ap_ssid_name FROM ssids_5ghz_radius");

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font face=\"Verdana\">\n"; 
echo "Choose SSID:";
echo "</font>";
echo "<form id=\"delete_ssid\" action=\"\" method=\"POST\">\n";
echo "<select name='ssidid'>";

    while ($ssidRow = $ssidDropdownQuery->fetch_assoc()) {

                  unset($ssidId, $ssidName);
                  $ssidId = $ssidRow['ap_ssid_id'];
                  $ssidName = $ssidRow['ap_ssid_name'];
                  echo '<option value="'.$ssidId.'">'.$ssidName.'</option>';

}

echo "</select>";

// Fetch POST data from file and execute Python commands & SQL queries
$varAPId = $_POST['apid'];
$varSSIDId = $_POST['ssidid'];

$apSql = "SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = '$varAPId'";
$apResult = $conn->query($apSql);

$ssidSql = "SELECT ap_ssid_name,ap_ssid_vlan,ap_ssid_radio_id,ap_ssid_ethernet_id FROM ssids_5ghz_radius WHERE ap_ssid_id = '$varSSIDId'";
$ssidResult = $conn->query($ssidSql);

// Get the data in place (so it can be passed to Python)

    // store data of each row
    while($row = $apResult->fetch_assoc()) {
       $queryIP = $row["ap_ip"];
       $queryUser = $row["ap_ssh_username"];
       $queryPass = $row["ap_ssh_password"];
    }

    while($row = $ssidResult->fetch_assoc()) {
       $querySSID = $row["ap_ssid_name"];
       $queryVlan = $row["ap_ssid_vlan"];
       $queryRadioSub = $row["ap_ssid_radio_id"];
       $queryGigaSub = $row["ap_ssid_ethernet_id"];
       $pyCommand = escapeshellcmd("python $scriptsDir/cisco_delete_ssid.py $queryIP $queryUser $queryPass $querySSID $queryVlan $queryRadioSub $queryGigaSub");
       $pyOutput = shell_exec($pyCommand);
       echo "<font face=\"Verdana\">\n";
       echo "<br>";
       echo "<br>";
       echo "Deletion of 5GHz RADIUS SSID <b>$querySSID</b> for Access Point <b>$apName</b> Successfully Initiated!";
       echo "</font>";
    }

echo "<font face=\"Verdana\">\n";
echo "<br>";
echo "<br>";
echo "<input type=\"submit\" value=\"Submit\">\n";
echo "</font>";

// Clear POST Variables
unset($_POST);

$conn->close();

?>
