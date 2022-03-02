#!/bin/bash
#!/usr/bin/env python3.5

INPUT_FILE=$1
SELECTED_COLUMNS=$2
OUTPUT_FILE=$3

zcat $INPUT_FILE | awk '{print $1, $2, $8}' > $SELECTED_COLUMNS

python select_ukbb_data.py $SELECTED_COLUMNS $OUTPUT_FILE
