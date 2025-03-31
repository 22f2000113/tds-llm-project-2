import re
import subprocess
from FileUtil import current_dir
from multipart import file_path


def get_sha_code(question):
    print("in get sha code")
    file_name_match = re.search(r"called (\S+\.md)", question)
    file_name = file_name_match.group(1) if file_name_match else None

    # Extract the command using regex
    #command_match = re.search(r"run (npx .+?sha256sum)", question)
    #command = command_match.group(1) if command_match else None
    file_path=current_dir+"/inputs/W1Q3/"+file_name
    print(f"q3 file path {file_path}")
    command = f"npx -y prettier@3.4.2 {file_path} | sha256sum"
    # Run the command and capture the output
    result = subprocess.run(command, shell=True, text=True, capture_output=True)

    # Print the result (SHA256 hash)
    print(result.stdout)
    return result.stdout.replace('\n','')
