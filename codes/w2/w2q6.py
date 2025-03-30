import requests
from FileUtil import read_file,current_dir, get_files_in_directory

URL = "https://vercel-app-ten-sable.vercel.app/api"
def get_verl_url():
    file_path = current_dir + "/inputs/W2Q6"
    files = get_files_in_directory(file_path)
    file_path +=  "/"+files[0]

    content = read_file(file_path)
    files = {'file': (files[0], content, 'application/json')}
    response = requests.post(URL, files=files)
    print(response.status_code)
    return URL

print(get_verl_url())