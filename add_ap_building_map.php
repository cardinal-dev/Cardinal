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

// Form to ask for Cardinal building map information
// Using heatmap.js to generate heatmaps for approximate AP coverage

echo "<html>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Location Name:</label>\n";
echo "<input type=\"text\" name=\"location_name\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Upload Building Map (e.g. PNG):</label>\n";
echo "<form action=\"add_building_png_upload.php\" method=\"post\" enctype=\"multipart/form-data\">\n";
echo "    <input type=\"file\" name=\"fileToUpload\" id=\"fileToUpload\">\n";
echo "<br />";
echo "<label>Heatmap Radius:</label>\n";
echo "<input type=\"text\" name=\"heatmap_radius\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Minimum Datapoint Value:</label>\n";
echo "<input type=\"text\" name=\"minimum_value\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Maximum Datapoint Value:</label>\n";
echo "<input type=\"text\" name=\"maximum_value\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>dB Value:</label>\n";
echo "<input type=\"text\" name=\"db_value\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>X Datapoint (Width):</label>\n";
echo "<input type=\"text\" name=\"x_datapoint\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Y Datapoint (Height):</label>\n";
echo "<input type=\"text\" name=\"y_datapoint\" required/>\n";
echo "<br /> </font>\n";
echo "<font face=\"Verdana\">\n";
echo "<input type=\"submit\" value=\"Submit\">\n";
echo "\n";
echo "</form>\n";
echo "</body>\n";
echo "</html>\n";

?>
