#!/bin/bash

# Create Cardinal Heatmap
# falcon78921

# Cardinal Configuration Variable Declarations

# IMPORTANT!: Modify this to include the proper location of cardinal_config.ini
cardinalBase=$(awk -F "=" '/cardinalbase/ {print $2}' /path/to/cardinal_config.ini)

# First, we generate the file from given information in add_new_heatmap.php

cat $cardinalBase/assets/templates/building_template.php > $cardinalBase/assets/building_maps/.php
mv $cardinalBase/assets/building_maps/.php $cardinalBase/assets/building_maps/$1.php

# Now, we need to modify file per variables

sed -i 's/$locationName/'$1'/g' $cardinalBase/assets/building_maps/$1.php
sed -i 's/$heatmapImage/'$2'/g' $cardinalBase/assets/building_maps/$1.php
