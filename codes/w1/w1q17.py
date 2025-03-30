import re
import subprocess
from FileUtil import  current_dir
def compare_files(question):
    # Regular expression to find all file names ending with .txt
    file_names = re.findall(r'\b\w+\.\w+\b', question)

    # Remove duplicates while preserving the order
    unique_list = []
    for item in file_names:
        if item not in unique_list:
            unique_list.append(item)
    print(current_dir)

    file_path=f"{current_dir}/inputs/W1Q17/"
    print(file_path+unique_list[0], file_path+unique_list[1])
    result = subprocess.run(['bash', 'w1q17.sh', file_path+unique_list[0], file_path+unique_list[1]], text=True, capture_output=True)
    return result.stdout

'''print(compare_files("Download and extract it. It has 2 nearly identical files, a.txt and b.txt, with the same number of lines. How many lines are different between a.txt and b.txt?"))'''