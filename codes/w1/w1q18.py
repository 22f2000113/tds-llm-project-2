from llm_api import get_result
import json
import re

def get_query(question):
    json_req = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": question},
            {"role": "system", "content": "Provide only required SQLite database query for the scenario mentioned in question. "}
        ]
    }
    print(f"Request body {json_req}")
    response = get_result(json_req)
    print(response.status_code)
    #print(response.content)
    res = json.loads(response.content)
    print(res)
    query = (res["choices"][0]["message"]["content"]).replace('sql','')
    text = re.sub(r'[`\n]', '', query)
    return query
