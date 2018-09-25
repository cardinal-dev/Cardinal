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

// HTML Dropdown for AP Group

$groupQuery = $conn->query("SELECT ap_group_id,ap_group_name FROM access_point_groups");

?>

<html>
<head>
</head>
<body>
<font face="Verdana">
Choose AP Group:
</font>
<form id="manage_ap_group" action="manage_ap_group_dashboard.php" method="POST">
<select name="groupid">

<?php

    while ($groupRow = $groupQuery->fetch_assoc()) {

                  unset($groupId, $groupName);
                  $groupId = $groupRow['ap_group_id'];
                  $groupName = $groupRow['ap_group_name'];
                  echo '<option value="'.$groupId.'">'.$groupName.'</option>';

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
