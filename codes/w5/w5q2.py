import re
from FileUtil import current_dir,get_files_in_directory

def get_unique_count():
    student_ids = set()
    file_path = current_dir+"/inputs/W5Q2"
    files =get_files_in_directory(file_path)
    file_path +="/"+files[0]
    with open(file_path, 'r') as file:
        for line in file:
            if len(line.strip()) > 0:
                student_id = re.findall(r'-\s*([A-Z0-9]{10})', line.strip())
                # Get unique student IDs by converting the list to a set
                print(student_id)
                student_ids.add(tuple(student_id))
    return str(len(student_ids))