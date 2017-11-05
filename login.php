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

// Start Cardinal Session

session_start();

// Cardinal MySQL Connection

require_once('includes/dbconnect.php');

$username = $_POST['username'];
$password = $_POST['password'];

// SQL Queries

$hashSql = "SELECT password FROM users WHERE username = '$username'";
$hashResult = $conn->query($hashSql);

    /* fetch associative array */
    while ($row = $hashResult->fetch_assoc()) {
        $queryHash = $row["password"];
    }

if (password_verify($password, $queryHash)) {
    $_SESSION['username'] = $_POST['username'];
    // Redirect to dashboard.php
    header('Location: dashboard.php');
} 

$conn->close();

?>

<html>
<head>
<title>Authorization Error</title>
</head>
<body>
<p>
You have failed to log into Cardinal. Please log in correctly to continue. 
</b>
<br>
Click Here to Retry: <a href="index.php">Login</a> </p>
</body>
</html>

