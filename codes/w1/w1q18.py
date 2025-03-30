from llm_api import get_result

def get_query(question):
    json = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": question},
            {"role": "system", "content": "Provide only required SQLite database query for the scenario mentioned in question. "}
        ]
    }
    response = get_result(json)
    return response.json(["choices"][0]["message"]["content"].replace('sql',''))

