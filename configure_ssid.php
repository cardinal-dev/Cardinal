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
$result = $conn->query("select ap_id,ap_name from access_points");

// HTML Dropdown for AP

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font face=\"Verdana\">\n"; 
echo "Choose AP:";
echo "</font>";
echo "<form id=\"configure_ap\" action=\"\" method=\"POST\">\n";
echo "<select name='id'>";

    while ($row = $result->fetch_assoc()) {

                  unset($id, $name);
                  $id = $row['ap_id'];
                  $name = $row['ap_name'];
                  echo '<option value="'.$id.'">'.$name.'</option>';

}

echo "</select>";
echo "<br>";
echo "</br>";

// Configure SSID Parameters

echo "<html>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>SSID Name:</label>\n";
echo "<input type=\"text\" name=\"ssid_name\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>WPA2-PSK (Minimum 8 Characters):</label>\n";
echo "<input type=\"password\" name=\"wpa2_psk\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>VLAN:</label>\n";
echo "<input type=\"text\" name=\"vlan\"/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Bridge Group ID:</label>\n";
echo "<input type=\"text\" name=\"bridge_group_id\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>2.4GHz Radio Sub Interface ID:</label>\n";
echo "<input type=\"text\" name=\"24_sub_id\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Gigabit Sub Interface ID:</label>\n";
echo "<input type=\"text\" name=\"giga_sub_id\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<input type=\"submit\" value=\"Submit\">\n";
echo "\n";
echo "</form>\n";
echo "</body>\n";
echo "</html>\n";

// Fetch POST data from configure_aps.html and execute SQL queries
$varConfID = $_POST['id'];

$sql = "SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = $varConfID";
$result = $conn->query($sql);

// Get the data in place (so it can be passed to Python)

if ($result->num_rows > 0) {
    // store data of each row
    while($row = $result->fetch_assoc()) {
       $queryIP = $row["ap_ip"];
       $queryUser = $row["ap_ssh_username"];
       $queryPass = $row["ap_ssh_password"];
       $querySSID = $_POST['ssid_name'];
       $queryWPA2 = $_POST['wpa2_psk'];
       $queryVlan = $_POST['vlan'];
       $queryBridgeGroup = $_POST['bridge_group_id'];
       $queryRadioSub = $_POST['24_sub_id'];
       $queryGigaSub = $_POST['giga_sub_id'];
       $pyCommand = escapeshellcmd("python $scriptsDir/cisco_configure_ssid.py $queryIP $queryUser $queryPass $querySSID $queryWPA2 $queryVlan $queryBridgeGroup $queryRadioSub $queryGigaSub");
       $pyOutput = shell_exec($pyCommand);

// Store SSID Data in Database 

       $ssidUpdate = "INSERT INTO ssids_24ghz (ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id) VALUES ('".$_POST["ssid_name"]."', '".$_POST["vlan"]."', '".$_POST["wpa2_psk"]."', '".$_POST["bridge_group_id"]."', '".$_POST["24_sub_id"]."', '".$_POST["giga_sub_id"]."')";
       $ssidQuery = mysqli_query($conn,$ssidUpdate);
       $ssidValue = mysqli_fetch_object($ssidQuery);
       echo "<br>";
       echo "<br>";
       echo "Creation of 2.4GHz SSID <b>$querySSID</b> for Access Point <b>$name</b> Successfully Initiated!";
       // Clear POST Variables
       unset($_POST);
     }
} else {
    echo "";
}

?>

<br>
<br>
<button onclick="window.location.href='/configure_ssid_wizard.php'">Back to Configure SSID Wizard</button>

<?php

$conn->close();

?>

