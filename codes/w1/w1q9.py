import json
import re

def sorted_json(question):
    json_pattern = r'\[.*\]'
    json_match = re.search(json_pattern, question)
    json_data = json.loads(json_match.group(0))
    field_names = re.findall(r'\b([a-zA-Z0-9_]+)\s+field\b', question)
    sorted_data = sorted(json_data, key=lambda x: (x[field_names[0]], x[field_names[1]]))
    return json.dumps(sorted_data)