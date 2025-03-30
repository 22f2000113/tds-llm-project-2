import subprocess
import  json
import re
def get_hash(question):
    match = re.search(r"Download\s+([a-zA-Z0-9_\-\.]+)", question)
    file_name = match.group(1)
    file_path = "./inputs/W1Q10/"+file_name
    print(file_path)
    key_value_pairs = {}
    # Read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any extra whitespace or newline characters and split by '='
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)  # Split into key and value
                key_value_pairs[key] = value

    json_string = json.dumps(key_value_pairs)
    result = subprocess.run(['node', 'hash.js', json_string], capture_output=True, text=True)
    return result.stdout
