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

// Cardinal Configuration

require_once('includes/cardinalconfig.php');

// We get our data from the previous page

$queryAPName = $_POST['heatmap_ap_name'];
$queryHeatmap = $_POST['Heatmap'];
$queryAPMinimum = $_POST['data_minimum'];
$queryAPMaximum = $_POST['data_maximum'];
$queryAPXCoord = $_POST['ap_x_coord'];
$queryAPYCoord = $_POST['ap_y_coord'];
$queryAPdB = $_POST['ap_dB_value'];

// Now, we pass to script and execute

$bashCommand = escapeshellcmd("$scriptsDir/create_heatmap_ap.sh $queryAPName $queryHeatmap $queryAPMinimum $queryAPMaximum $queryAPXCoord $queryAPYCoord $queryAPdB");
$bashOutput = shell_exec($bashCommand);


// Link back to the add_new_heatmap_ap.php page

echo "<font face=\"Verdana\">\n";
echo "Access Point Plotted on <b>$queryHeatmap</b> Heatmap Successfully!";
echo "<br>";
echo "<br>";
echo "<a href=\"add_new_heatmap_ap.php\">Back to Add New Heatmap AP</a>";
echo "</font>";


?>
