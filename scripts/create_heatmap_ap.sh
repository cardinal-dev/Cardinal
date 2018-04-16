#!/bin/bash

# Create Cardinal Heatmap AP
# falcon78921

# Cardinal Configuration Variable Declarations

# IMPORTANT!: Modify this to include the proper location of cardinal_config.ini
cardinalBase=$(awk -F "=" '/cardinalbase/ {print $2}' /path/to/cardinal_config.ini)

# Append the information sent from the add_new_ap_heatmap.php page to the following heatmap page
# Start from reverse, each access point will go below the Cardinal APS GO BELOW HERE comment 

sed -i '/Cardinal APS GO BELOW HERE/aheatmapInstance.addData('$1')' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/a}' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/avalue: '$7'' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/ay: '$6',' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/ax: '$5',' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/amax: '$4',' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/amin: '$3',' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/avar '$1' = {' $cardinalBase/assets/building_maps/$2
sed -i '/Cardinal APS GO BELOW HERE/a<!-- '$1' datapoint -->' $cardinalBase/assets/building_maps/$2
