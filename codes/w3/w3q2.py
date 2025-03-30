from llm_api import get_result
import re
def get_tokens(question):
    user_message_pattern = r'(?<=Specifically, when you make a request to OpenAI\'s GPT-4o-Mini with just this user message:\n)(.*?)(?=\n\.\.\. how many input tokens does it use up\?)'

    match = re.search(user_message_pattern, question, re.DOTALL)
    user_message = match.group(1)
    json = {"model": "gpt-4o-mini",
            "messages": [
                { "role": "user",
                 "content": user_message
                 }
            ]
    }
    response = get_result(json)
    return int(response["usage"]["prompt_tokens"])

