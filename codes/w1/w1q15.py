import re
import subprocess
from FileUtil import current_dir

# Input string
def get_file_size(question):
    # Regular expression to extract the string to replace and its replacement
    pattern = r'at least (\d+) bytes.*modified on or after ([A-Za-z]{3}, \d{2} [A-Za-z]{3}, \d{4}, \d{1,2}:\d{2} [apm]+ [A-Za-z]+)'

    # Search for the pattern
    match = re.search(pattern, question)

    # Extract the strings to be replaced and the replacement string
    if match:
        byte_size = match.group(1)  # Extract the number of bytes
        date = match.group(2)  # Extract the date
        print(f" files at least : {byte_size}")
        print(f"modified on or after Tue,: {date}")
        # Run the bash script with the extracted strings as arguments
        result = subprocess.run(
    ['bash', "w1q15.sh", byte_size, date, "./inputs/W1Q15"],capture_output=True, text=True)
        #print("Return code:", result.returncode)
        #print("stdout:", result.stdout)
        #print("stderr:", result.stderr)
        return str(result.stdout)

