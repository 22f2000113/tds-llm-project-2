import os
import subprocess
import re
from FileUtil import create_repo,GITHUB_URL
import  shutil

def add_file(repo_url,file_name,email_data):
    # Path where we want to clone the repository locally
    clone_dir = './W1Q13/'

    if os.path.exists(clone_dir) and os.path.isdir(clone_dir):
        shutil.rmtree(clone_dir)
    # Clone the repository
    subprocess.run(['git', 'clone', repo_url, clone_dir])

    # Change the current working directory to the cloned repository
    os.chdir(clone_dir)

    # Create the email.json file with the specified content
    with open(file_name, 'w') as f:
        f.write(email_data)

    # Stage the new file for commit
    subprocess.run(['git', 'add', file_name])

    # Commit the new file
    subprocess.run(['git', 'commit', '-m', f'Add {file_name} file with email address'])

    # Push the changes to GitHub
    subprocess.run(['git', 'push', 'origin', 'main'])


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
        repo_url = f'{GITHUB_URL}/{repo_name}.git'
        add_file(repo_url =repo_url,file_name=file_name,email_data=email_data)
        return f"https://raw.githubusercontent.com/22f2000113/{repo_name}/main/{file_name}"


