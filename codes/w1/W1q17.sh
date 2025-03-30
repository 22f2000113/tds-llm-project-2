

input_directory1=$1
input_directory2=$2

#diff $input_directory1 $input_directory2 |wc -l

with open(input_directory1, 'r') as file1, open(input_directory2, 'r') as file2:
    # Read all lines from both files
    file1_lines = file1.readlines()
    file2_lines = file2.readlines()

# Find the minimum length of the two files
min_len = min(len(file1_lines), len(file2_lines))

# Initialize a counter for different lines
different_lines_count = 0

# Compare the lines one by one
for i in range(min_len):
    if file1_lines[i] != file2_lines[i]:
        different_lines_count += 1

# If the files have different lengths, count the extra lines
different_lines_count += abs(len(file1_lines) - len(file2_lines))

# Output the result
echo $different_lines_count
