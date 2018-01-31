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

// Query SQL Database for up-to-date SSID count

$ssids24GhzSql = $conn->query("SELECT COUNT(*) FROM ssids_24ghz");
$ssids24GhzRow = $ssids24GhzSql->fetch_row();
$ssids24Ghz = $ssids24GhzRow[0];

$ssids24GhzRadiusSql = $conn->query("SELECT COUNT(*) FROM ssids_24ghz_radius");
$ssids24GhzRadiusRow = $ssids24GhzRadiusSql->fetch_row();
$ssids24GhzRadius = $ssids24GhzRadiusRow[0];

$ssids5GhzSql = $conn->query("SELECT COUNT(*) FROM ssids_5ghz");
$ssids5GhzRow = $ssids5GhzSql->fetch_row();
$ssids5Ghz = $ssids5GhzRow[0];

$ssids5GhzRadiusSql = $conn->query("SELECT COUNT(*) FROM ssids_5ghz_radius");
$ssids5GhzRadiusRow = $ssids5GhzRadiusSql->fetch_row();
$ssids5GhzRadius = $ssids5GhzRadiusRow[0];


// Calculate the results (combined number of SSIDs registered)

$queryTotalSsids = $ssids24Ghz + $ssids24GhzRadius + $ssids5Ghz + $ssids5GhzRadius;

$conn->close();

?>

<html>
<link rel="stylesheet" href="assets/css/metro.css">

<div class="metroblock ssids left ">
  <h1><?php echo $queryTotalSsids; ?></h1>
  <div class="clear"></div>
  <h2>SSIDs</h2>
</div>
