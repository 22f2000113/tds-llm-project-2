import re
import  json
def get_payload(question):
    pattern = r"(\w+)\s\((\w+)\)"

    # Find all matches in the text
    matches = re.findall(pattern, question)

    # Convert matches into a dictionary of field names and their data types
    fields = {field: data_type for field, data_type in matches}

    json_structure = {}
    for field, data_type in fields.items():
        json_structure[field] = {
            "type": data_type
        }

    key_list = list(fields.keys())


    req_props = json.dumps(key_list, indent=4)
    # Convert the structure to a JSON string and print it
    props = json.dumps(json_structure, indent=4)

    return '''{"model": "gpt-4o-mini", "messages": [{"role": "system", "content": "Respond in JSON"}, {"role": "user", "content": "Generate 10 random addresses in the US"}], "response_format": {"type": "json_schema", "json_schema": {"name": "generate_addresses", "schema": {"type": "object", "properties": {"addresses": {"type": "array", "items": {"type": "object", "properties":'''+props+''', "required": '''+req_props+''', "additionalProperties": False}}}}}}}'''

