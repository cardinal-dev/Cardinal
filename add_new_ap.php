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

// Add new access point form

echo "<html>\n";
echo "<form id=\"add_new_ap\" action=\"functions/add_new_ap_calc.php\" method=\"POST\">\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Access Point Name:</label>\n";
echo "<input type=\"text\" name=\"ap_name\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Access Point IP Address:</label>\n";
echo "<input type=\"text\" name=\"ap_ip\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";

// HTML Dropdown for choosing access point group 

echo "<label>Access Point Group:</label>\n";

$result = $conn->query("select ap_group_id,ap_group_name from access_point_groups");

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<form id=\"configure_ap_group\">\n";
echo "<select name='group_id'>";

    while ($row = $result->fetch_assoc()) {

                  unset($id, $name);
                  $id = $row['ap_group_id'];
                  $name = $row['ap_group_name'];
                  echo '<option value="'.$id.'">'.$name.'</option>';

}

echo "</select>";
echo "<br />";
echo "<font face=\"Verdana\">\n";
echo "<label>SSH Username:</label>\n";
echo "<input type=\"text\" name=\"ssh_username\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>SSH Password:</label>\n";
echo "<input type=\"password\" name=\"ssh_password\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>SNMP Community:</label>\n";
echo "<input type=\"password\" name=\"ap_snmp\" required/>\n";
echo "<br /> </font>\n";
echo "\n";
echo "<input type=\"submit\" value=\"Register\">\n";
echo "</form>\n";
echo "</body>\n";
echo "</script>\n";
echo "</html>\n";

$conn->close();

// Success after access point registration (from add_new_ap_calc.php)
if ( isset($_GET['Success']) && $_GET['Success'] == 1 )
{
     // Success Message!
     echo "<br>";
     echo "<br>";
     echo "Access Point Registered Successfully!";
}

?>
