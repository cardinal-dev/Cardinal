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

// First, we need to give our location a name. We'll start a form

echo "<html>\n";
echo "<font face=\"Verdana\">\n"; 
echo "<form id=\"configure_heatmap\" action=\"add_new_heatmap_calc.php\" method=\"POST\">\n";
echo "<label>Location Name:</label>\n";
echo "<input type=\"text\" name=\"location_name\" required/>\n";
echo "<br>";

// Then, we need to select one of our uploaded images to act as the heatmap location 

echo "<font face=\"Verdana\">\n"; 
echo "Choose Heatmap Image: ";

echo "<select name=\"ImageFile\">\n";
echo "<option value=\"\">- Select Image -\n";

$dirPath = dir('assets/img');
$imgArray = array();
while (($file = $dirPath->read()) !== false)

// This statement will only display files that have a GIF, JPG, or PNG file extension

{
  if ((substr($file, -3)=="gif") || (substr($file, -3)=="jpg") || (substr($file, -3)=="png"))

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
echo "<br>";
echo "<input type=\"submit\" value=\"Submit\">\n";
echo "</form>";
echo "</html>";

?>


