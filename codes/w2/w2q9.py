import pandas as pd
from typing import List
from FileUtil import current_dir, get_files_in_directory

def get_json(params):
    file_path = current_dir + "/inputs/W2Q9/"
    files = get_files_in_directory(file_path)
    students_df = pd.read_csv(files[0])
    """
    Endpoint to return all students or filter by class.
    If the class parameter is provided, only students in those classes are returned.
    """

    print("params ", params)
    print("List ", List[str])
    if params:
        # Filter students by the given classes
        filtered_students = students_df[students_df['class'].isin(params)]
    else:
        # If no class filter is given, return all students
        filtered_students = students_df

    # Convert the filtered dataframe to a list of dictionaries and return it
    return {"students": filtered_students.to_dict(orient="records")}