import subprocess
import re
import json

def get_command(question):
    url_pattern = r'https?://[^\s]+'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Extract URL and email
    url = re.search(url_pattern, question).group(0)
    email = re.search(email_pattern, question).group(0)
    print( f"{url}/get?email={email}")
    command = ["uv", "run", "--with", "httpie", "--", "https", f"{url}?email={email}"]
    result = subprocess.run(command, capture_output=True, text=True)
    json_data = json.loads(result.stdout)
    return json.dumps(json_data)

