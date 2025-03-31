import re

def get_payload_request(question):
    pattern = r'^[a-zA-Z0-9\s]{5,}$'

    # Split the text into lines
    lines = question.split('\n')

    # Extract lines that match the pattern
    meaningless_lines = [line.strip() for line in lines if re.match(pattern, line.strip())]

    converted_text = '\\n'.join(meaningless_lines)

    payload = '''
    import httpx
    import json
    api_key = "open_api_key_text"
    
    def get_sentiments():
      response = httpx.post(
          "https://api.openai.com/v1/chat/completions",
           headers={"Authorization":f"Bearer {api_key}"},
           json ={"model":"gpt-4o-mini",
                 "messages" :[
                     {"role":"system","content":"Analyze the sentiment of the following text and categorize it as GOOD, BAD, or NEUTRAL."},
                     {"role":"user","content":"'''+converted_text+'''"}
                 ]
    
          }
      )
      response.raise_for_status()
      return response.json()
    
    print(get_sentiments())'''

    return payload
