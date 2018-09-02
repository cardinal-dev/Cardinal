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

// HTML Dropdown for AP

$apDropdownQuery = $conn->query("SELECT ap_id,ap_name FROM access_points");

?>

<html>
<head>
</head>
<body>
<font face="Verdana">
Choose AP:
</font>
<form id="manage_aps" action="manage_aps_dashboard.php" method="POST">
<select name="apid">

<?php

    while ($apRow = $apDropdownQuery->fetch_assoc()) {

                  unset($apId, $apName);
                  $apId = $apRow['ap_id'];
                  $apName = $apRow['ap_name'];
                  echo '<option value="'.$apId.'">'.$apName.'</option>';

}

?>

</select>
<br>
<br>
<input type="Submit" label="Submit">
</body>
</form>
</html>

<?php

$conn->close();

?>
