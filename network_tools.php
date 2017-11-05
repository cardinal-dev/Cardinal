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

echo "<html>\n";
echo "<body>\n";
echo "<form id=\"network_tools\" action=\"\" method=\"POST\">\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Hostname/IP Address:</label>\n";
echo "<input type=\"text\" name=\"network_ip\" required/>\n";
echo "<br /> </font>\n";
echo "</form>\n";

echo "<input type=\"button\" value=\"Nmap Scan\" name=\"nmap\" onclick=\"askForNmap()\" />\n";
echo "<input type=\"button\" value=\"Ping\" name=\"ping\" onclick=\"askForPing()\" />\n";
echo "<input type=\"button\" value=\"Traceroute\" name=\"tracert\" onclick=\"askForTracert()\" />\n";
echo "<input type=\"button\" value=\"Dig\" name=\"dig\" onclick=\"askForDig()\" />\n";
echo "<input type=\"button\" value=\"Whois Lookup\" name=\"whois\" onclick=\"askForWhois()\" />\n";
echo "<input type=\"button\" value=\"Curl\" name=\"curl\" onclick=\"askForCurl()\" />\n";

echo "<script>\n";
echo "form=document.getElementById(\"network_tools\");\n";
echo "function askForNmap() {\n";
echo "        form.action=\"network_tools_nmap.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForPing() {\n";
echo "        form.action=\"network_tools_ping.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForTracert() {\n";
echo "        form.action=\"network_tools_tracert.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForDig() {\n";
echo "        form.action=\"network_tools_dig.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForWhois() {\n";
echo "        form.action=\"network_tools_whois.php\";\n";
echo "        form.submit();\n";
echo "}\n";
echo "function askForCurl() {\n";
echo "        form.action=\"network_tools_curl.php\";\n";
echo "        form.submit();\n";
echo "}\n";

echo "</script>\n";
echo "</body>\n";
echo "</html>";

?>
