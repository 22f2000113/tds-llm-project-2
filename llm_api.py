import  requests
import os
from fastapi import HTTPException
url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
headers = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {AIPROXY_TOKEN}"
}

def get_result(json):
    """Calls AI proxy to generate Python code for the given task."""
    return requests.post(
        url=url,
        headers=headers,
        json=json
    )

def get_result_format(task, system_prompt, response_format):
    """Calls AI proxy to generate Python code for the given task."""
    response = requests.post(
            url=url,
            headers=headers,
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": task},
                    {"role": "system", "content": system_prompt}
                ],
                "response_format": response_format
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="AI Proxy request failed")

    return response

def get_embedding(texts):
    url = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"  # Correct API URL

    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "text-embedding-3-small",  # Ensure model name is correct
        "input": texts,  # Accepts list of strings
        "encoding_format": "float"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return None

    return response.json()