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

// Form for the deletion of 5GHz SSIDs

$result = $conn->query("select ap_ssid_id,ap_ssid_name from ssids_5ghz");

echo "<html>\n";
echo "<head>\n";
echo "</head>\n";
echo "<body>\n";
echo "<font face=\"Verdana\">\n";
echo "Choose 5GHz SSID:";
echo "<br>";
echo "<br>";
echo "</font>";
echo "<form id=\"delete_ssid_5ghz_data\" action=\"\" method=\"POST\">\n";
echo "<select name='ssid5id'>";

    while ($row = $result->fetch_assoc()) {

                  unset($id, $name);
                  $id = $row['ap_ssid_id'];
                  $name = $row['ap_ssid_name'];
                  echo '<option value="'.$id.'">'.$name.'</option>';
 
}

echo "</select>";
echo "<input type=\"button\" value=\"Delete 5GHz SSID\" name=\"delete_ssid_5ghz_mysql\" onclick=\"askForSsid5Delete()\" />\n";
echo "</form>\n";
echo "<script>\n";
echo "form=document.getElementById(\"delete_ssid_5ghz_data\");\n";
echo "function askForSsid5Delete() {\n";
echo "        form.action=\"delete_ssid_db_5ghz.php\";\n";
echo "        form.submit();\n";
echo "}\n";

echo "</script>\n";
echo "</body>\n";
echo "</html>";

$conn->close();

?>

<button onclick="window.location.href='/delete_ssid_wizard.php'">Back to Delete SSID Wizard</button>
