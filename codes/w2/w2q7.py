import base64
from FileUtil import create_repo,upload_files_to_repo


def create_file():
    content = '''
     name: GitActionAssign
     on:
        push:
            branches:
                - main
     jobs:
        test:
            runs-on: ubuntu-latest
            steps:
                - name: 22f2000113@ds.study.iitm.ac.in
                  run: echo "Hello, world!"
      '''
    encoded_content = base64.b64encode(content.encode()).decode()
    return encoded_content


def create_email_action():
    # GitHub token for authentication (generate it in your GitHub account settings)
    repo_name = "w2-q7"
    repo_created = create_repo(repo_name)
    # Check if the repository was created successfully
    if repo_created:
        file_path = ".github/workflows/github-actions-demo.yml"
        file_content = create_file()
        upload_files_to_repo(repo_name, file_name=file_path, file_encoded_content=file_content)
        return f"https://github.com/22f2000113/{repo_name}/"
        

print(create_email_action())

