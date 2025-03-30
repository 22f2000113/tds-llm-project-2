from FileUtil import current_dir,get_files_in_directory
import json
import  re

def count_key_occurrences(data, key_name):
    count = 0

    if isinstance(data, dict):  # If it's a dictionary
        if key_name in data:
            count += 1  # Count the key if it exists
        # Recurse for all dictionary values
        for value in data.values():
            count += count_key_occurrences(value, key_name)

    elif isinstance(data, list):  # If it's a list
        for item in data:
            count += count_key_occurrences(item, key_name)

    return count

def get_key_count(question):
    file_path = current_dir + "/inputs/W5Q7"
    files = get_files_in_directory(file_path)
    file_path += "/" + files[0]
    with open(file_path, 'r') as file:
        data = json.load(file)
    key_pattern = r"\b([A-Za-z0-9]+)\b(?=\s+appear\s+as\s+a\s+key)"

    # Find the key in the text
    match = re.search(key_pattern, question)

    key_to_search =match.group(1)

    return str(count_key_occurrences(data, key_to_search))