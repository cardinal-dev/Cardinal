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

function db_connect() {

        // Define connection as a static variable, to avoid connecting more than once 
    static $conn;

        // Try and connect to the database, if a connection has not been established yet
    if(!isset($conn)) {
             // Load configuration as an array. Use the actual location of your configuration file
        $config = parse_ini_file('/home/cardinal/cardinalmysql.ini'); // CHANGE THIS TO THE APPROPRIATE LOCATION!
        $conn = mysqli_connect($config['servername'],$config['username'],$config['password'],$config['dbname']);
    }

        // If connection was not successful, handle the error
    if($conn === false) {
            // Handle error - notify administrator, log to a file, show an error screen, etc.
        return mysqli_connect_error(); 
    }
    return $conn;
}

// Connect to the database
$conn = db_connect();

// Query configuration information

$cardinalConfig = "SELECT cardinal_home,cardinal_scripts,cardinal_tftp,poll_schedule FROM settings WHERE settings_id = 1";
$configResult = $conn->query($cardinalConfig);

if ($configResult->num_rows > 0) {
    // store data of each row
    while($settingsRow = $configResult->fetch_assoc()) {
       $cardinalHome = $settingsRow['cardinal_home'];
       $scriptsDir = $settingsRow['cardinal_scripts'];
       $cardinalTftp = $settingsRow['cardinal_tftp'];
       $pollSchedule = $settingsRow['poll_schedule'];
     }
} else {
    echo "";
}

?> 
