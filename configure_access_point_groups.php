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
$result = $conn->query("select ap_group_id,ap_group_name from access_point_groups");

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font face=\"Verdana\">\n";
echo "Choose AP Group:";
echo "<br>";
echo "</font>";
echo "<form id=\"manage_ap\" action=\"\" method=\"POST\">\n";
echo "<select name='id'>";

    while ($row = $result->fetch_assoc()) {

                  unset($id, $name);
                  $id = $row['ap_group_id'];
                  $name = $row['ap_group_name'];
                  echo '<option value="'.$id.'">'.$name.'</option>';
 
}

echo "</select>";
echo "<input type=\"button\" value=\"Ping AP Group\" name=\"ping\" onclick=\"askForPing()\" />\n";
echo "<input type=\"button\" value=\"Fetch AP Group Uptime\" name=\"uptime\" onclick=\"askForUptime()\" />\n";
echo "<input type=\"button\" value=\"Reboot AP Group\" name=\"reboot\" onclick=\"askForReboot()\" />\n";
echo "<input type=\"button\" value=\"Fetch AP Group Info\" name=\"info\" onclick=\"askForInfo()\" />\n";
echo "<input type=\"button\" value=\"Find Me! Group\" name=\"findme\" onclick=\"askForFindMe()\" />\n";
echo "<input type=\"button\" value=\"Flash AP Group\" name=\"flash\" onclick=\"askForFlash()\" />\n";
echo "<input type=\"button\" value=\"Save AP Group Changes\" name=\"save\" onclick=\"askForSave()\" />\n";
echo "</form>\n";
echo "<script>\n";
echo "form=document.getElementById(\"manage_ap\");\n";
echo "function askForPing() {\n";
echo "        form.action=\"fetch_ping_group.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForUptime() {\n";
echo "        form.action=\"fetch_uptime_group.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForReboot() {\n";
echo "        form.action=\"reboot_ap_group.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForInfo() {\n";
echo "        form.action=\"fetch_ap_info_group.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForFindMe() {\n";
echo "        form.action=\"find_me_group.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForFlash() {\n";
echo "        form.action=\"flash_ap_group.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForSave() {\n";
echo "        form.action=\"do_wr_group.php\";\n";
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
