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

require_once('includes/cardinalconfig.php');
$result = $conn->query("select ap_group_id,ap_group_name from access_point_groups");

// HTML Dropdown for AP

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font face=\"Verdana\">\n"; 
echo "Choose AP Group:";
echo "</font>";
echo "<form id=\"configure_ap\" action=\"\" method=\"POST\">\n";
echo "<select name='id'>";

    while ($row = $result->fetch_assoc()) {

                  unset($id, $name);
                  $id = $row['ap_group_id'];
                  $name = $row['ap_group_name'];
                  echo '<option value="'.$id.'">'.$name.'</option>';

}

echo "</select>";
echo "<br>";
echo "</br>";

// Configure SSID Parameters

echo "<html>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>TFTP IP:</label>\n";
echo "<input type=\"text\" name=\"tftp-ip\" required/>\n";
echo "<br /> </font>\n";
echo "<input type=\"submit\" value=\"Submit\">\n";
echo "\n";
echo "</form>\n";
echo "</body>\n";
echo "</html>\n";

// Fetch POST data from configure_aps.html and execute SQL queries
$varConfID = $_POST['id'];

$sql = "SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = $varConfID";
$result = $conn->query($sql);

// Get the data in place (so it can be passed to Python)

if ($result->num_rows > 0) {
    // store data of each row
    while($row = $result->fetch_assoc()) {
       $queryIP = $row["ap_ip"];
       $queryUser = $row["ap_ssh_username"];
       $queryPass = $row["ap_ssh_password"];
       $queryTFTP = $_POST['tftp-ip'];
       $pyCommand = escapeshellcmd("python $scriptsDir/cisco_tftp_backup_group.py $queryIP $queryUser $queryPass $queryTFTP");
       $pyOutput = shell_exec($pyCommand);
       echo "<font face=\"Verdana\">\n";
       echo "Access Point Configuration Backup for Group $name Initiated!";
       echo "</font>";
     }
} else {
    echo "";
}

$conn->close();

?>

