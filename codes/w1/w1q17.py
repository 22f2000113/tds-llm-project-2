import re
import subprocess
from FileUtil import  current_dir
def compare_files(question):
    # Regular expression to find all file names ending with .txt
    file_names = re.findall(r'\b\w+\.txt\b', question)

    # Remove duplicates while preserving the order
    unique_list = []
    for item in file_names:
        if item not in unique_list:
            unique_list.append(item)
    print(current_dir)

    file_path=f"{current_dir}/inputs/W1Q17/"
    print(unique_list[0], unique_list[1])
    result = subprocess.run(['bash', './code/w1/w1q17.sh', "./inputs/W1Q17/",unique_list[0], unique_list[1]], text=True, capture_output=True)
    return result.stdout.replace('\n','')

