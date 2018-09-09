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
						<a href="https://cardinal.mcclunetechnologies.net">Developer</a>
					</li>

					<li>
						<a href="https://github.com/falcon78921/Cardinal">Source</a>
					</li>

					<li>
						<a href="https://github.com/falcon78921/Cardinal/issues">Technical Support</a>
					</li>

					<li>
						<a href="logout.php">Logout</a>
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
						Access Point Statistics
					</div>


					<div class="chart-stage">
						<div id="grid-1-1">
							<iframe height="310px" scrolling="no" src="graph_total_aps.php" style="border:none;" width="300px"></iframe> <iframe height="310px" scrolling="no" src="graph_ap_clients.php" style="border:none;" width="300px"></iframe> <iframe height="310px" scrolling="no" src="graph_ap_groups.php" style="border:none;" width="300px"></iframe><iframe height="310px" scrolling="no" src="graph_total_ssids.php" style="border:none;" width="300px"></iframe>
						</div>
					</div>


					<div class="chart-notes">
						Cardinal access point statistics
					</div>
				</div>
			</div>


			<div class="col-sm-12">
				<div class="chart-wrapper">
					<div class="chart-title">
						Add Access Point
					</div>


					<div class="chart-stage">
						<center>
							<a class="add_new_ap" href="add_new_ap.php"><img src="assets/img/cardinal1.png"></a>
						</center>
					</div>


					<div id="addnewap" style="display:none;" title="Add New Access Point">
						<iframe height="350" id="add_new_ap_frame" name="add_new_ap_frame" width="350"></iframe>
					</div>
					<script>
					        $(document).ready(function () {
					        $(".add_new_ap").click(function () {
					        $("#add_new_ap_frame").attr('src', $(this).attr("href"));
					        $("#addnewap").dialog({
					            width: 400,
					            height: 450,
					            modal: true,
					            close: function () {
					        $("#add_new_ap_frame").attr('src', "about:blank");
					       }
					   });
					   return false;
					});
					});

					</script>

					<div class="chart-notes">
						Add access points to Cardinal
					</div>
				</div>
			</div>


			<div class="col-sm-12">
				<div class="chart-wrapper">
					<div class="chart-title">
						Add Access Point Group
					</div>


					<div class="chart-stage">
						<center>
							<a class="add_new_ap_group" href="add_access_point_groups.php"><img src="assets/img/cardinal2.png"></a>
						</center>
					</div>


					<div id="addnewapgroup" style="display:none;" title="Add New Access Point Group">
						<iframe height="350" id="add_new_ap_group_frame" name="add_new_ap_group_frame" width="350"></iframe>
					</div>
					<script>
					 $(document).ready(function () {
					     $(".add_new_ap_group").click(function () {
					     $("#add_new_ap_group_frame").attr('src', $(this).attr("href"));
					     $("#addnewapgroup").dialog({
					       width: 400,
					       height: 450,
					       modal: true,
					       close: function () {
					           $("#add_new_ap_group_frame").attr('src', "about:blank");
					       }
					   });
					   return false;
					});
					});

					</script>

					<div class="chart-notes">
						Add access point groups to Cardinal
					</div>
				</div>
			</div>

                        <div class="col-sm-12">
                                <div class="chart-wrapper">
                                        <div class="chart-title">
                                                Delete Access Point
                                        </div>


                                        <div class="chart-stage">
                                                <center>
                                                        <a class="delete_aps" href="delete_aps.php"><img src="assets/img/cardinal10.png"></a>
                                                </center>
                                        </div>


                                        <div id="deleteaps" style="display:none;" title="Delete Access Points">
                                                <iframe height="350" id="delete_ap_frame" name="delete_ap_frame" width="350"></iframe>
                                        </div>
                                        <script>
                                        $(document).ready(function () {
                                        $(".delete_aps").click(function () {
                                           $("#delete_ap_frame").attr('src', $(this).attr("href"));
                                           $("#deleteaps").dialog({
                                               width: 400,
                                               height: 450,
                                               modal: true,
                                               close: function () {
                                                   $("#delete_ap_frame").attr('src', "about:blank");
                                               }
                                           });
                                           return false;
                                        });
                                        });

                                        </script>

                                        <div class="chart-notes">
                                                Delete access points from Cardinal
                                        </div>
                                </div>
                        </div>

                        <div class="col-sm-12">
                                <div class="chart-wrapper">
                                        <div class="chart-title">
                                                Delete Access Point Group
                                        </div>


                                        <div class="chart-stage">
                                                <center>
                                                        <a class="delete_ap_group" href="delete_ap_group.php"><img src="assets/img/cardinal10.png"></a>
                                                </center>
                                        </div>


                                        <div id="deleteapgroup" style="display:none;" title="Delete Access Point Groups">
                                                <iframe height="350" id="delete_ap_group_frame" name="delete_ap_group_frame" width="350"></iframe>
                                        </div>
                                        <script>
                                        $(document).ready(function () {
                                        $(".delete_ap_group").click(function () {
                                           $("#delete_ap_group_frame").attr('src', $(this).attr("href"));
                                           $("#deleteapgroup").dialog({
                                               width: 400,
                                               height: 450,
                                               modal: true,
                                               close: function () {
                                                   $("#delete_ap_group_frame").attr('src', "about:blank");
                                               }
                                           });
                                           return false;
                                        });
                                        });

                                        </script>

                                        <div class="chart-notes">
                                                Delete access point groups from Cardinal
                                        </div>
                                </div>
                        </div>


			<div class="col-sm-12">
				<div class="chart-wrapper">
					<div class="chart-title">
						Network Toolkit
					</div>


					<div class="chart-stage">
						<center>
							<a class="network_tools" href="network_tools.php"><img src="assets/img/cardinal14.png"></a>
						</center>
					</div>


					<div id="networktools" style="display:none;" title="Cardinal Network Toolkit">

						<iframe height="768" id="network_tools_frame" name="network_tools_frame" width="1366"></iframe>

					</div>
					<script>
					        $(document).ready(function () {
					        $(".network_tools").click(function () {
					        $("#network_tools_frame").attr('src', $(this).attr("href"));
					        $("#networktools").dialog({
					            width: 1366,
					            height: 768,
					            modal: true,
					            close: function () {
					        $("#network_tools_frame").attr('src', "about:blank");
					       }
					   });
					   return false;
					});
					});

					</script>

					<div class="chart-notes">
						Run network diagnostic tools
					</div>
				</div>
			</div>


			<div class="col-sm-12">
				<div class="chart-wrapper">
					<div class="chart-title">
						Manage Cardinal Access Points
					</div>


					<div class="chart-stage">
						<center>
							<a class="manage_aps" href="manage_aps_wizard.php"><img src="assets/img/cardinal4.png"></a>
						</center>
					</div>


					<div id="manageaps" style="display:none;" title="Manage Cardinal Access Points">
						<iframe height="768" id="manage_aps_frame" name="manage_aps_frame" width="1366"></iframe>
					</div>
					<script>
					 $(document).ready(function () {
					     $(".manage_aps").click(function () {
					     $("#manage_aps_frame").attr('src', $(this).attr("href"));
					     $("#manageaps").dialog({
					       width: 1366,
					       height: 768,
					       modal: true,
					       close: function () {
					           $("#manage_aps_frame").attr('src', "about:blank");
					       }
					   });
					   return false;
					});
					});

					</script>

					<div class="chart-notes">
						Manage Cardinal access points
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
							<a class="tftp_backup_group" href="backup_ap_config_group.php"><img src="assets/img/cardinal6.png"></a>
						</center>
					</div>


					<div id="tftpbackupgroup" style="display:none;" title="TFTP Backup (Group)">
						<iframe height="350" id="tftp_backup_group_frame" name="tftp_backup_group_frame" width="350"></iframe>
					</div>
					<script>
					$(document).ready(function () {
					$(".tftp_backup_group").click(function () {
					   $("#tftp_backup_group_frame").attr('src', $(this).attr("href"));
					   $("#tftpbackupgroup").dialog({
					       width: 400,
					       height: 450,
					       modal: true,
					       close: function () {
					           $("#tftp_backup_group_frame").attr('src', "about:blank");
					       }
					   });
					   return false;
					});
					});

					</script>

					<div class="chart-notes">
						Backup An Entire Access Point Group's Configuration Via TFTP
					</div>
				</div>
			</div>

			<div class="col-sm-6 col-md-4">
				<div class="chart-wrapper">
					<div class="chart-title">
						Configure SSIDs
					</div>


					<div class="chart-stage">
						<center>
							<a class="configure_ssids" href="configure_ssid_wizard.php"><img src="assets/img/cardinal5.png"></a>
						</center>
					</div>


					<div id="configuressids" style="display:none;" title="Configure SSIDs">
						<iframe height="350" id="configure_ssids_frame" name="configure_ssids_frame" width="350"></iframe>
					</div>
					<script>
					$(document).ready(function () {
					$(".configure_ssids").click(function () {
					   $("#configure_ssids_frame").attr('src', $(this).attr("href"));
					   $("#configuressids").dialog({
					       width: 400,
					       height: 450,
					       modal: true,
					       close: function () {
					           $("#configure_ssids_frame").attr('src', "about:blank");
					       }
					   });
					   return false;
					});
					});

					</script>

					<div class="chart-notes">
						Configure SSIDs for registered access points in Cardinal
					</div>
				</div>
			</div>

			<div class="col-sm-6 col-md-4">
				<div class="chart-wrapper">
					<div class="chart-title">
						Delete SSIDs
					</div>


					<div class="chart-stage">
						<center>
							<a class="delete_ssids" href="delete_ssid_wizard.php"><img src="assets/img/cardinal10.png"></a>
						</center>
					</div>


					<div id="deletessids" style="display:none;" title="Delete SSIDs">
						<iframe height="350" id="delete_ssids_frame" name="delete_ssids_frame" width="350"></iframe>
					</div>
					<script>
					$(document).ready(function () {
					$(".delete_ssids").click(function () {
					   $("#delete_ssids_frame").attr('src', $(this).attr("href"));
					   $("#deletessids").dialog({
					       width: 400,
					       height: 450,
					       modal: true,
					       close: function () {
					           $("#delete_ssids_frame").attr('src', "about:blank");
					       }
					   });
					   return false;
					});
					});

					</script>

					<div class="chart-notes">
						Delete a SSID from Cardinal
					</div>
				</div>
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

