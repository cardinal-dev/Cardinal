#!/bin/bash

# Create Cardinal Heatmap AP
# falcon78921

# Cardinal Configuration Variable Declarations

# IMPORTANT!: Modify this to include the proper location of cardinal_config.ini
cardinalBase=$(awk -F "=" '/cardinalbase/ {print $2}' /path/to/cardinal_config.ini)

# Append the information sent from the add_new_ap_heatmap.php page to the following heatmap page
# Start from reverse, each access point will go below the Cardinal APS GO BELOW HERE comment 

sed -i '/Cardinal APS GO BELOW HERE/aecho "\n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "heatmapInstance.addData('"$1"');\n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "};\n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "  value: '"$7"' // the value at datapoint(x, y)\n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "  y: '"$6"', // y coordinate of the datapoint, a number\n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "  x: '"$5"', // x coordinate of the datapoint, a number \n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "  max: '"$4"', \n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "  min: '"$3"',\n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "var '"$1"' = {\n";' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/aecho "// '"$1"' datapoint\n";' $cardinalBase/assets/building_maps/$2

