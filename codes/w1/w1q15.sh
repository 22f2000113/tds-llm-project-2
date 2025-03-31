#!/bin/bash

# Directory to search (use current directory if none specified)
DIR="."
cd
# Minimum size in bytes
MIN_SIZE=$1
# Date to compare against
TARGET_DATE=$2
input_directory=$3
current_directory=$(pwd)
cd $input_directory

# Convert the target date to a timestamp for comparison
TARGET_TIMESTAMP=$(date -d "$TARGET_DATE" +%s)

# Initialize total size
total_size=0

# Iterate over each file in the directory (including subdirectories) and check conditions
for file in $(find "$DIR" -type f); do
    # Get file size
    file_size=$(stat -c %s "$file")

    # Get file's last modification time in the required format (e.g., 'Tue, 20 Jul, 1993, 9:26 pm IST')
    file_date=$(stat -c %y "$file")

    # Convert file modification date to timestamp
    file_timestamp=$(date -d "$file_date" +%s)

    # Check if file meets the size and date conditions
    if [[ $file_size -ge $MIN_SIZE && $file_timestamp -ge $TARGET_TIMESTAMP ]]; then
        # Add to total size
        total_size=$((total_size + file_size))
    fi
done

# Output the total size of matching files
echo $total_size
