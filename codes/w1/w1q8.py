# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
# ]
# ///
import re
import pandas as pd
import os

def get_number_from_csv(question,file_path):
    pattern = r'[\w-]+\.csv'

    file_name = re.findall(pattern, question)
    # Step 4: Read the CSV file and get the value from the "answer" column
    print(f"file name: {file_name[0]}")
    #csv_file_path = os.path.join(file_path, file_name[0])
    df = pd.read_csv(file_path+f"/{file_name[0]}")
    return df['answer'].iloc[0]