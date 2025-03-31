
input_directory=$1
cd $input_directory
EMPTY_FOLDER="renamed_files"

mkdir -p $EMPTY_FOLDER

# Step 4: Move all files from the extracted folder into the empty folder
find . -type f -exec mv {} $EMPTY_FOLDER/ \;

# Step 5: Rename all files by replacing each digit with the next (1 becomes 2, 9 becomes 0)
cd $EMPTY_FOLDER
for file in *; do
    # Initialize the new filename
    new_name=""

    # Loop through each character in the filename
    for (( i=0; i<${#file}; i++ )); do
        char="${file:$i:1}"  # Extract one character at a time

        # Check if the character is a digit
        if [[ "$char" =~ [0-9] ]]; then
            # Replace digit with the next one (1 becomes 2, 9 becomes 0)
            next_char=$(( (char + 1) % 10 ))
            new_name+="$next_char"  # Append the modified character
        else
            # Append the non-digit character without modification
            new_name+="$char"
        fi
    done

    # Rename the file with the modified name
    mv "$file" "$new_name"
done

# Step 6: Run grep . * | LC_ALL=C sort | sha256sum on the renamed folder
grep . * | LC_ALL=C sort | sha256sum