import subprocess
import  json
import re
from FileUtil import current_dir,get_files_in_directory

def get_hash(question):
    #match = re.search(r"Download\s+([a-zA-Z0-9_\-\.]+)\s+", question)
    file_path = current_dir+"/inputs/W1Q10/"

    files = get_files_in_directory(file_path)
    file_path+=files[0]
    print(f"file path in w1q10 {file_path}")

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
    
    result = subprocess.run(['node', './codes/w1/hash.js', json_string], capture_output=True, text=True)
    return result.stdout.replace('\n','')
