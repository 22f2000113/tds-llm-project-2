import re
from FileUtil import current_dir,get_files_in_directory

pattern = r'"sales":(\d+)'

# Function to extract sales number from each line in the file
def get_total_sales():
    file_path = current_dir + "/inputs/W5Q6"
    files = get_files_in_directory(file_path)
    file_path += "/" + files[0]
    total_sales = 0
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(pattern, line)

            # Check if a match is found and extract the sales number
            if match:
                sales_number = int(match.group(1))
                total_sales += sales_number
            else:
                print("Sales number not found")
        return str(int(total_sales))



