import re

def get_payload_request(question):
    pattern = r".* One of the test cases involves sending a sample piece of meaningless text:\s*(.*?)\s* Write a Python program"
    # Search for the pattern
    match = re.search(pattern, question, re.DOTALL)

    meaningless_text = match.group(1)
    converted_text = meaningless_text.replace("\n", "\\n")

    pattern1 = r'.* analyze the sentiment of this \(meaningless\) text into (.*?)(\.)'

    # Search for the pattern
    match1 = re.search(pattern1, question)
    extracted_text = match1.group(1)

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
                     {"role":"system","content":"Analyze the sentiment of the following text and categorize it as'''+extracted_text+'''."},
                     {"role":"user","content":"'''+converted_text+'''"}
                 ]
    
          }
      )
      response.raise_for_status()
      return response.json()
    
    print(get_sentiments())'''

    return payload
