import  re
import json
def get_json_body(question):
    pattern = r"Dear user, please verify your transaction code \d+ sent to [\w@.]+"

    # Find all matches of the pattern in the text
    verification_messages = re.findall(pattern, question)
    formatted_messages = ', '.join([f'"{message}"' for message in verification_messages])
    output = '''{"model": "text-embedding-3-small", "input": ['''+formatted_messages+'''   ] }'''
    # Output the extracted verification messages
    '''for message in verification_messages:
        output = output+"\""+message+"\"\n"
        print(message)
    print(output)
    output=output+'''

    return json.dumps(output)

