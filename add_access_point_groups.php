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
echo "<form method=\"post\" action=\"add_access_point_groups_calc.php\">\n";
echo "<font face=\"Verdana\">\n";
echo "<label>Access Point Group Name:</label>\n";
echo "<input type=\"text\" name=\"ap_group_name\" required/>\n";
echo "<br /> </font>\n";
echo "<input type=\"submit\" value=\"Register\">\n";
echo "\n";
echo "</form>\n";
echo "</body>\n";
echo "</html>\n";

// Success after access point registration (from add_new_ap_calc.php)
if ( isset($_GET['Success']) && $_GET['Success'] == 1 )
{
     // Success Message!
     echo "<font face=\"Verdana\">\n";
     echo "Access Point Group Registered Successfully!";
     echo "</font>";
}

?>
