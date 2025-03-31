from fastapi import HTTPException
from subprocess import run
from io import BytesIO
import zipfile
import requests
import os
import subprocess
import json


current_dir = os.path.abspath(os.path.dirname(__file__))
GITHUB_API_URL = 'https://api.github.com/user/repos' 

GITHUB_USERNAME = "22f2000113"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

GITHUB_URL  = f'https://github.com/{GITHUB_USERNAME}'

def set_repo(repo_user_name):
    GITHUB_USERNAME=repo_user_name
    GITHUB_TOKEN = os.getenv(f'({repo_user_name}_GITHUB_TOKEN')
   

def read_file(file_path):
    print("file_path "+file_path)
    """Reads a file and returns its content."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File does not exist")

def write_file(file_name, content, content_type ):
    """Writes content to a file."""
    mode ='w'
    if isinstance(content, bytes) and content_type != 'image/webp':
        # Convert bytes to string (assuming UTF-8 encoding)
        content = content.decode('utf-8')

    if content_type == 'text/markdown' or content_type == 'image/webp':
        mode = 'wb'
    with open(file_name,mode) as file:
        file.write(content)

def task_executor(file_name, params):
    """Executes the generated Python script with dependencies."""
    python_code = params['python_code']
    python_dependencies = params['python_dependencies']
    if python_dependencies:
        metadata_script = (
            "# /// script\n"
            "# requires-python = \">=3.11\"\n"
            "# dependencies = [\n"
            + "\n".join([f'#     "{dependency["module"]}",' for dependency in python_dependencies])
            + "\n# ]\n"
            "# ///"
        )
    else :
        metadata_script=''
    write_file(file_name, metadata_script + "\n" + python_code)

  
    
def execute_file(file_name,**kws):
    try:
        return run(["uv", "run", file_name], capture_output=True, text=True, cwd=os.getcwd())        
    except Exception as e:
        print("Exception in task_executor "+str(e))
        return {"error": str(e)}


def call_python_script(script_name, *args):
    # Construct the command to execute the script with arguments
    command = ["uv", "run", script_name] + list(args)
    # Run the subprocess with the command
    run(command, capture_output=True, text=True)
    print(f"complted  script execution")

def extract_zip_file(file_path,zip_file: BytesIO):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(file_path)
        return [name for name in zip_ref.namelist()]

def extract_file(file_path,content):
    with zipfile.ZipFile(BytesIO(content)) as zip_ref:
        # List the contents of the ZIP file to check what it contains
        zip_ref.printdir()

        # Extract all files (assuming only one file inside the ZIP)
        zip_ref.extractall(file_path)



def add_file(repo_url,file_name,email_data):
    # Path where we want to clone the repository locally
    clone_dir = './inputs/W1Q13/'
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


def create_repo(repo_name):
    # GitHub token for authentication (generate it in your GitHub account settings)


    # Headers for the request
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Data for creating the repository (public and no description)
    data = {
        'name': repo_name,
        'private': False,  # Public repository
        'description': 'A public repo for email.json file',
    }

    # Send a POST request to create the repository
    response = requests.post(GITHUB_API_URL, json=data, headers=headers)
    # Check if the repository was created successfully
    print(response.status_code)
    if response.status_code == 201:
        return True


def upload_files_to_repo(repo_name,file_name,file_encoded_content):
    # GitHub API URL for repository content
    CONTENT_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/contents/{file_name}"



    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "message": "Add initial file",
        "content": file_encoded_content,
    }

    # Upload the index.html file to the repository
    response = requests.put(CONTENT_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print("index.html file uploaded successfully!")
    else:
        print(f"Error uploading file: {response.json()}")

def get_files_in_directory(file_path):
    files = os.listdir(file_path)

    # Filter out directories and keep only files
    files = [file for file in files if os.path.isfile(os.path.join(file_path, file))]
    return files
