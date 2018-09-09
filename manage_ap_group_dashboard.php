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

require_once('includes/cardinalconfig.php');

// Fetch POST data from file and execute Python commands & SQL queries
$varGroupId = $_POST['groupid'];

$groupSql = "SELECT ap_name,ap_group_name,ap_ip,ap_total_clients FROM access_points,access_point_groups WHERE access_point_groups.ap_group_id = '$varGroupId'";
$groupResult = $conn->query($groupSql);

    // store data of each row
    while($row = $groupResult->fetch_assoc()) {
       $groupName = $row["ap_group_name"];
    }

$_SESSION['groupid'] = $varGroupId;

?>

<html>
<head>
	<title>Cardinal</title>
	<meta content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no' name='viewport'>
	<link href="assets/css/bootstrap.min.css" rel="stylesheet" type="text/css">
	<link href="assets/css/cardinal-dashboard.css" rel="stylesheet" type="text/css">
	<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/base/jquery-ui.css" rel="stylesheet" type="text/css">
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js">
	</script>
	<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js">
	</script>
</head>

<body class="application">
	<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
		<div class="container-fluid">
			<div class="navbar-header">
				<button class="navbar-toggle" data-target=".navbar-collapse" data-toggle="collapse" type="button"><span class="sr-only">Toggle navigation</span> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span></button> <a class="navbar-brand" href="./dashboard.php">Cardinal</a>
			</div>


			<div class="navbar-collapse collapse">
				<ul class="nav navbar-nav navbar-left">
					<li>
						<a href="./">Home</a>
					</li>


					<li>
						<a href="http://cardinal.mcclunetechnologies.net">Developer</a>
					</li>


					<li>
						<a href="https://github.com/falcon78921">Source</a>
					</li>


					<li>
						<a href="https://github.com/falcon78921">Technical Support</a>
					</li>
				</ul>
			</div>
		</div>
	</div>


	<div class="container-fluid">
		<div class="row">
			<div class="col-sm-12">
				<div class="chart-wrapper">
					<div class="chart-title">
						Access Point Group Statistics for <?php echo $groupName; ?>
					</div>


					<div class="chart-stage">
						<div id="grid-1-1">
						<iframe height="310px" scrolling="no" src="graph_per_ap_clients.php" style="border:none;" width="300px"></iframe>
						</div>
					</div>


					<div class="chart-notes">
						Cardinal Access Point Group Statistics for <?php echo $groupName; ?>
					</div>
				</div>
			</div>

                        <div class="col-sm-6 col-md-4">
                                <div class="chart-wrapper">
                                        <div class="chart-title">
                                                TFTP Backup (Group)
                                        </div>


                                        <div class="chart-stage">
                                                <center>
                                                        <a class="tftp_backup" href="backup_ap_config_group.php"><img src="assets/img/cardinal6.png"></a>
                                                </center>
                                        </div>


                                        <div id="tftpbackup" style="display:none;" title="TFTP Backup">
                                                <iframe height="350" id="tftp_backup_frame" name="tftp_backup_frame" width="350"></iframe>
                                        </div>
                                        <script>
                                        $(document).ready(function () {
                                        $(".tftp_backup").click(function () {
                                           $("#tftp_backup_frame").attr('src', $(this).attr("href"));
                                           $("#tftpbackup").dialog({
                                               width: 400,
                                               height: 450,
                                               modal: true,
                                               close: function () {
                                                   $("#tftp_backup_frame").attr('src', "about:blank");
                                               }
                                           });
                                           return false;
                                        });
                                        });

                                        </script>

                                        <div class="chart-notes">
                                                
                                        </div>
                                </div>
                        </div>


	<link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/base/jquery-ui.css" rel="stylesheet" type="text/css">
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js">
	</script> 
	<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js">
	</script>
</body>
</html>

