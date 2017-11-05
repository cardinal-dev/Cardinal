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

require_once('includes/dbconnect.php');

$sql="SELECT * FROM access_points";

if ($result=mysqli_query($conn,$sql))
  {
  // Return the number of rows in result set
  $rowcount=mysqli_num_rows($result);
  // Free result set
  mysqli_free_result($result);
  }


echo "<!doctype html>\n";
echo "<html>\n";
echo "\n";
echo "<head>\n";
echo "    <title>Pie Chart</title>\n";
echo "    <script src=\"assets/js/Chart.bundle.js\"></script>\n";
echo "    <script src=\"assets/js/utils.js\"></script>\n";
echo "</head>\n";
echo "\n";
echo "<body>\n";
echo "    <div id=\"canvas-holder\" style=\"width:300px\">\n";
echo "        <canvas id=\"chart-area\" />\n";
echo "    </div>\n";
echo "    <script>\n";
echo "    var randomScalingFactor = function() {\n";
echo "        return Math.round(Math.random() * 100);\n";
echo "    };\n";
echo "\n";
echo "    var config = {\n";
echo "        type: 'pie',\n";
echo "        data: {\n";
echo "            datasets: [{\n";
echo "            data: ['$rowcount'],\n";
echo "            backgroundColor: [\n";
echo "                \"#FF6384\",\n";
echo "                \"#36A2EB\",\n";
echo "                \"#FFCE56\"\n";
echo "            ],\n";
echo "                backgroundColor: [\n";
echo "                    window.chartColors.red,\n";
echo "                ],\n";
echo "                label: 'Dataset 1'\n";
echo "            }],\n";
echo "            labels: [\n";
echo "                \"Total Number of Access Points Registered\",\n";
echo "            ]\n";
echo "        },\n";
echo "        options: {\n";
echo "            responsive: true\n";
echo "        }\n";
echo "    };\n";
echo "\n";
echo "    window.onload = function() {\n";
echo "        var ctx = document.getElementById(\"chart-area\").getContext(\"2d\");\n";
echo "        window.myPie = new Chart(ctx, config);\n";
echo "    };\n";
echo "\n";
echo "    document.getElementById('randomizeData').addEventListener('click', function() {\n";
echo "        config.data.datasets.forEach(function(dataset) {\n";
echo "            dataset.data = dataset.data.map(function() {\n";
echo "                return randomScalingFactor();\n";
echo "            });\n";
echo "        });\n";
echo "\n";
echo "        window.myPie.update();\n";
echo "    });\n";
echo "\n";
echo "    var colorNames = Object.keys(window.chartColors);\n";
echo "    document.getElementById('addDataset').addEventListener('click', function() {\n";
echo "        var newDataset = {\n";
echo "            backgroundColor: [],\n";
echo "            data: [],\n";
echo "            label: 'New dataset ' + config.data.datasets.length,\n";
echo "        };\n";
echo "\n";
echo "        for (var index = 0; index < config.data.labels.length; ++index) {\n";
echo "            newDataset.data.push(randomScalingFactor());\n";
echo "\n";
echo "            var colorName = colorNames[index % colorNames.length];;\n";
echo "            var newColor = window.chartColors[colorName];\n";
echo "            newDataset.backgroundColor.push(newColor);\n";
echo "        }\n";
echo "\n";
echo "        config.data.datasets.push(newDataset);\n";
echo "        window.myPie.update();\n";
echo "    });\n";
echo "\n";
echo "    document.getElementById('removeDataset').addEventListener('click', function() {\n";
echo "        config.data.datasets.splice(0, 1);\n";
echo "        window.myPie.update();\n";
echo "    });\n";
echo "    </script>\n";
echo "</body>\n";
echo "\n";
echo "</html>\n";

$conn->close();

?>
