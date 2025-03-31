#!/bin/bash

# Arguments passed from Python script
string_to_replace=$1
replacement_string=$2
input_directory=$3  # The directory containing the files
current_directory=$(pwd)

cd $input_directory
#echo "Current directory is: $current_directory"


# Loop through all files in the provided directory and replace the text
for file in *; do
  #echo $file
  if [ -f "$file" ]; then
    # Perform the replacement in the file using sed
    sed -i "s/$string_to_replace/$replacement_string/Ig" "$file"
  fi
done
#current_directory=$(pwd)
# Calculate and display the hash of all files using sha256sum
cat * | sha256sum
