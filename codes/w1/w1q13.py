import re
import base64
from FileUtil import create_repo,GITHUB_URL,upload_files_to_repo
import json

def create_file(email_data):
    encoded_content = base64.b64encode(str(email_data).encode()).decode()
    return encoded_content


def create_email_repo(question):
    # GitHub token for authentication (generate it in your GitHub account settings)
    repo_name = "w1_q13"
    repo_created = create_repo(repo_name)

    file_info_pattern = r"called (\S+\.json) with the value ({.*})"

    # Search for the pattern in the text
    match = re.search(file_info_pattern, question)

    # Extract file name and content

    file_name = match.group(1)
    email_data = match.group(2)
    # Check if the repository was created successfully
    if repo_created:
        file_content = create_file(email_data)
        upload_files_to_repo(repo_name, file_name, file_content)
        return f"https://raw.githubusercontent.com/22f2000113/{repo_name}/main/{file_name}"


