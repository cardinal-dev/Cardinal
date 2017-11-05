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

$result = $conn->query("select ap_id,ap_name from access_points");

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font face=\"Verdana\">\n";
echo "Choose AP:";
echo "<br>";
echo "</font>";
echo "<form id=\"manage_ap\" action=\"\" method=\"POST\">\n";
echo "<select name='id'>";

    while ($row = $result->fetch_assoc()) {

                  unset($id, $name);
                  $id = $row['ap_id'];
                  $name = $row['ap_name'];
                  echo '<option value="'.$id.'">'.$name.'</option>';
 
}

echo "</select>";
echo "<input type=\"button\" value=\"Ping\" name=\"ping\" onclick=\"askForPing()\" />\n";
echo "<input type=\"button\" value=\"Fetch Uptime\" name=\"uptime\" onclick=\"askForUptime()\" />\n";
echo "<input type=\"button\" value=\"Reboot\" name=\"reboot\" onclick=\"askForReboot()\" />\n";
echo "<input type=\"button\" value=\"Fetch Info\" name=\"info\" onclick=\"askForInfo()\" />\n";
echo "<input type=\"button\" value=\"Fetch ARP Table\" name=\"arp\" onclick=\"askForArp()\" />\n";
echo "<input type=\"button\" value=\"Find Me!\" name=\"find-me\" onclick=\"askForLed()\" />\n";
echo "<input type=\"button\" value=\"Flash AP\" name=\"flash-ap\" onclick=\"askForOverwrite()\" />\n";
echo "<input type=\"button\" value=\"Save AP Changes\" name=\"perform-wr\" onclick=\"askForWr()\" />\n";
echo "</form>\n";
echo "<script>\n";
echo "form=document.getElementById(\"manage_ap\");\n";
echo "function askForPing() {\n";
echo "        form.action=\"fetch_ping.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForUptime() {\n";
echo "        form.action=\"fetch_uptime.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForReboot() {\n";
echo "        form.action=\"reboot_ap.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForInfo() {\n";
echo "        form.action=\"fetch_ap_info.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForArp() {\n";
echo "        form.action=\"fetch_arp.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForLed() {\n";
echo "        form.action=\"find_me.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForOverwrite() {\n";
echo "        form.action=\"flash_ap.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForWr() {\n";
echo "        form.action=\"do_wr.php\";\n";
echo "        form.submit();\n";
echo "}\n";

echo "</script>\n";
echo "</body>\n";
echo "</html>";


$result2 = mysqli_query($conn,"SELECT * FROM access_points,access_point_groups");

echo "<font face=\"Verdana\">\n";
echo "<table border='1'>
<tr>
<th>ID:</th>
<th>AP Name:</th>
<th>AP IP:</th>
<th>AP Group:</th>
</tr>";

while($row = mysqli_fetch_array($result2))
{
echo "<tr>";
echo "<td>" . $row['ap_id'] . "</td>";
echo "<td>" . $row['ap_name'] . "</td>";
echo "<td>" . $row['ap_ip'] . "</td>";
echo "<td>" . $row['ap_group_name'] . "</td>";
echo "</tr>";
}
echo "</table>";
echo "</font>\n";

mysqli_close($conn);

?>
