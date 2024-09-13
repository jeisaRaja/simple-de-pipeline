#!/bin/bash

# Define the base directory
BASE_DIR="data"

# Define the directories containing CSV files
DIRS=("load" "raw" "transform")

# Define files to exclude from deletion
EXCLUDE_FILES=("ElectronicsProductsPricingData.csv")

# Iterate over each directory
for dir in "${DIRS[@]}"; do
    echo "Removing CSV files in $BASE_DIR/$dir, excluding: ${EXCLUDE_FILES[@]}"

    # Find and remove all CSV files in the directory, excluding the specified files
    find "$BASE_DIR/$dir" -type f -name "*.csv" ! -name "${EXCLUDE_FILES[0]}" -exec rm -f {} +

    echo "Completed removing CSV files in $BASE_DIR/$dir"
done

echo "Specified CSV files have been removed, except those excluded."

