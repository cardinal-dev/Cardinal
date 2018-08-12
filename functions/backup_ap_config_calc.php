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

require_once(__DIR__ . '/../includes/cardinalconfig.php');

// MySQL connection information

require_once(__DIR__ . '/../includes/dbconnect.php');

// Fetch AP Session

$varAPId = $_SESSION['apid'];

// MySQL calculations for access point command

$tftpBackupQuery = mysqli_query($conn,"SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_id = $varAPId");

// Get the data in place (so it can be passed to Python)

    // store data of each row
    while($row = mysqli_fetch_array($tftpBackupQuery)) {
       $queryIP = $row["ap_ip"];
       $queryUser = $row["ap_ssh_username"];
       $queryPass = $row["ap_ssh_password"];
       $queryTFTP = $_POST['tftp-ip'];
       $queryTFTPName = $_POST['config-name'];
       $pyCommand = escapeshellcmd("python $scriptsDir/cisco_tftp_backup.py $queryIP $queryUser $queryPass $queryTFTP $queryTFTPName");
       $pyOutput = shell_exec($pyCommand);
       echo "<font face=\"Verdana\">\n";
       echo "Access Point Configuration Backup Initiated!";
       echo "</font>";
    }

// Link back to the backup_ap_config.php page
echo "<br>";
echo "<br>";
echo "<a href=\"../backup_ap_config.php\">Back to TFTP Backup Menu</a>";
echo "</font>";

$conn->close();

?>
