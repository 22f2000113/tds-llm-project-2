import  json
import requests
import base64
from FileUtil import create_repo,upload_files_to_repo,GITHUB_TOKEN,GITHUB_USERNAME

def create_file():
    content = '''
    <html>
      <h1>Hi</h1>
      <!--email_off-->22f2000113@ds.study.iitm.ac.in<!--/email_off-->
    </html>
    '''
    encoded_content = base64.b64encode(content.encode()).decode()
    return encoded_content


def enable_github_pages(repo_name):
    pages_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/pages"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }

    response = requests.post(pages_url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print(f"GitHub Pages enabled for {repo_name}!")
        print(f"Your site is live at https://{GITHUB_USERNAME}.github.io/{repo_name}/")
        return f"https://{GITHUB_USERNAME}.github.io/{repo_name}/"
    else:
        print(f"Error enabling GitHub Pages: {response.json()}")



def create_email_repo():
    # GitHub token for authentication (generate it in your GitHub account settings)
    repo_name = "w2-q3-site1"
    repo_created = create_repo(repo_name)
    # Check if the repository was created successfully
    if repo_created:
        file_content =  create_file()
        upload_files_to_repo(repo_name, "index.html", file_content)
        return enable_github_pages(repo_name)



