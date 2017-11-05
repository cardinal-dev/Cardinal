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

echo "<!doctype html>\n";
echo "<html>\n";
echo "<head>\n";
echo "<meta charset=\"utf-8\">\n";
echo "<title>$locationName</title>\n";
echo "<script src='../js/heatmap.js'></script>\n";
echo "</head>\n";
echo "<body>\n";
echo "<style type = \"text/css\">\n";
echo "body {\n";
echo "    background-image: url(\"../img/$heatmapImage\");\n";
echo "    background-color: #cccccc;\n";
echo "    background-repeat: no-repeat;\n";
echo "    background-attachment: fixed;\n";
echo "    background-position: centered;\n";
echo "}\n";
echo "</style>\n";
echo "  <div id='heatMap' style=\"height: 742px\">\n";
echo "    <canvas width=\"1024px\" height=\"742px\" style=\"position:absolute; left: 0; top: 0\"></canvas>\n";
echo "</div>\n";
echo "</body>\n";
echo "<script> \n";
echo "// create configuration object\n";
echo "var config = {\n";
echo "  container: document.getElementById('heatMap'),\n";
echo "  radius: 120,\n";
echo "  maxOpacity: .5,\n";
echo "  minOpacity: 0,\n";
echo "  blur: .75\n";
echo "};\n";
echo "// create heatmap with configuration\n";
echo "var heatmapInstance = h337.create(config);\n";
echo "\n";

// Cardinal APS GO BELOW HERE



echo "</script>\n";
echo "</html>";

?>
