import  tabula
import pandas as pd
from FileUtil import current_dir,get_files_in_directory
import re
import os

def extract_info(text):
    # Regular expression patterns
    subject_pattern = r"total ([A-Za-z]+) marks"
    group_range_pattern = r"groups (\d+)-(\d+)"
    min_marks_pattern = r"(\d+)\s+or\s+more\s+marks\s+in\s+([A-Za-z]+)"

    # Extracting subject
    subject_match = re.search(subject_pattern, text)
    subject = subject_match.group(1) if subject_match else None

    # Extracting group range
    group_range_match = re.search(group_range_pattern, text)
    group_start, group_end = (group_range_match.group(1), group_range_match.group(2)) if group_range_match else \
    (None, None)

    # Extracting minimum marks
    min_marks_match = re.search(min_marks_pattern, text)
    min_marks = min_marks_match.group(1) if min_marks_match else None
    min_marks_subject = min_marks_match.group(2) if min_marks_match else None

    return subject, (group_start, group_end), min_marks, min_marks_subject

file_path = current_dir + "/inputs/W4Q9"
def get_marks_file(range):
    print(range)
    if os.path.exists( file_path+"/output.csv"):
        # Remove the file
        os.remove( file_path+"/output.csv")
    files = get_files_in_directory(file_path)
    tabula.convert_into(file_path+"/" + files[0], file_path+"/output.csv", output_format="csv", pages=range)


def get_marks(question):
    subject, group_range, min_marks, min_marks_subject = extract_info(question)
    get_marks_file(f"{group_range[0]}-{group_range[1]}")
    # Display extracted information
    print(f"Subject: {subject}")
    print(f"Group Range: {group_range[0]} to {group_range[1]}")
    print(f"Minimum Marks Required: {min_marks} marks in {min_marks_subject}")

    df = pd.read_csv(file_path+"/output.csv")


    # Convert Economics column to numeric (handle errors if non-numeric data exists)
    df[subject] = pd.to_numeric(df[subject], errors="coerce")

    #print(df.info)

    # Filter students who scored 10 or more in Economics
    filtered_students = df[df[subject] >= int(0)]
    #print(filtered_students)
    # Calculate the total Economics marks
    total_marks = filtered_students[subject].sum()

    return (int(total_marks))


