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

require_once(__DIR__ . '/../includes/cardinalconfig.php');

// Delete SSID from Cardinal database
$varSsidId = $_POST['ssid24id'];

// Query database for Cardinal record. Delete record when found
$sql = "DELETE FROM ssids_24ghz WHERE ap_ssid_id = '$varSsidId'";

if ($conn->query($sql) === TRUE) {
    echo "";
} else {
    echo "Error deleting record: " . $conn->error;
}

// Confirmation that the SSID was successfully deleted from Cardinal database
echo "<font face=\"Verdana\">\n";
echo "2.4GHz SSID Successfully Deleted!";

// Link back to the delete_ssid_database.php
echo "<br>";
echo "<br>";
echo "<a href=\"delete_ssid_database.php\">Back to Cardinal SSID Deletion Menu</a>";
echo "</font>";

$conn->close();

?>

