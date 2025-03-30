import re
import subprocess

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
        result = subprocess.run(
    ['bash', "w1q14.sh", string_to_replace, replacement_string, "./inputs/W1Q14"],capture_output=True, text=True)
        return result.stdout
