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

// First, we need some information regarding positioning the AP. Please check your heatmap for location. As of this release, I did not
// develop a drag & drop method. I am working on this (using interact.js). However, you can use the Page Ruler (Google Chrome Extension) to get approximate 
// measurements for placing AP on heatmap.

echo "<html>";
echo "<font face=\"Verdana\">\n";
echo "<form id=\"add_ap_heatmap\" action=\"add_new_heatmap_ap_calc.php\" method=\"POST\">\n";
echo "<label>AP Name:</label>\n";
echo "<input type=\"text\" name=\"heatmap_ap_name\" required/>\n";
echo "<br>";

// Then, we need to select one of our created heatmaps

echo "<font face=\"Verdana\">\n"; 
echo "Choose Heatmap: ";

echo "<select name=\"Heatmap\">\n";
echo "<option value=\"\">- Select Heatmap -\n";

$dirPath = dir('assets/building_maps');
$imgArray = array();
while (($file = $dirPath->read()) !== false)

// This statement will only display files that have a PHP file extension

{
  if ((substr($file, -3)=="php") || (substr($file, -3)=="php") || (substr($file, -3)=="php"))

{
   $imgArray[ ] = trim($file);
  }
}

$dirPath->close();
sort($imgArray);
$c = count($imgArray);
for($i=0; $i<$c; $i++)
{
    echo "<option value=\"" . $imgArray[$i] . "\">" . $imgArray[$i] . "\n";
}

echo "</select>";

// Now, we finish the rest of the form

echo "<font face=\"Verdana\">\n";
echo "<br />";
echo "<label>Data Minimum:</label>\n";
echo "<input type=\"text\" name=\"data_minimum\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Data Maximum:</label>\n";
echo "<input type=\"text\" name=\"data_maximum\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>X-Coordinate Datapoint:</label>\n";
echo "<input type=\"text\" name=\"ap_x_coord\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Y-Coordinate Datapoint:</label>\n";
echo "<input type=\"text\" name=\"ap_y_coord\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Data Value (in dB):</label>\n";
echo "<input type=\"text\" name=\"ap_dB_value\" required/>\n";
echo "<br /> </font>\n";
echo "<input type=\"submit\" value=\"Submit\">\n";
echo "\n";
echo "</form>\n";
echo "</html>\n";

?>

