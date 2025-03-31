import re
import subprocess
import os
# Input string
def get_file_hash(question):
    # Regular expression to extract the string to replace and its replacement
    pattern = r'replace all "(.*?)" \(in.*\) with "(.*?)"'

    # Search for the pattern in the text
    match = re.search(pattern, question)

    # Extract the strings to be replaced and the replacement string
    if match:
        string_to_replace = match.group(1)
        replacement_string = match.group(2)
        print(f"String to replace: {string_to_replace}")
        print(f"Replacement string: {replacement_string}")
        # Run the bash script with the extracted strings as arguments
        script_path = "w1q14.sh"
        full_path = os.path.abspath(script_path)

        print("Full path of the script:", full_path)
        result = subprocess.run(
    ['bash', "./codes/w1/w1q14.sh", string_to_replace, replacement_string, "./inputs/W1Q14"],capture_output=True, text=True)
        print(f"result of w1q14 question {result.stdout}")
        print("Return code:", result.returncode)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

        return result.stdout
