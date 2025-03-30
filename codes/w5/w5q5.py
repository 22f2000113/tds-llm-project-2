import json
import pandas as pd
import re
from FileUtil import current_dir,get_files_in_directory

def product_count(question):

    pattern = r"(?:The product sold is (\w+))|(?:The number of units sold [A-Za-z\s]+ (\d+))|(?:in\s([A-Za-z\s]+)\sCity)"

    matches = re.findall(pattern, question)

    # Extracting the results
    item_sold = matches[0][0]  # Product sold
    units_sold = matches[1][1]  # Units sold
    city_name = matches[2][2]  # City name

    file_path = current_dir + "/inputs/W5Q5"
    files = get_files_in_directory(file_path)
    file_path += "/" + files[0]
    with open(file_path, 'r') as file:
        data = json.load(file)

    filtered_data1 = [entry for entry in data if entry['city'].startswith(city_name[0:3]) ]

    # Filter cities starting with 'Mexi' and specify a product, e.g., "Shoes"
    filtered_data = [entry for entry in data if entry['city'].startswith(city_name[0:3]) and entry['product'] == item_sold]

    print(filtered_data1)# Create a DataFrame from the filtered data
    filtered_df = pd.DataFrame(filtered_data)

    # Display filtered data
    print("Filtered Cities and Products:")
    print(filtered_df[['city', 'product', 'sales']])
    return str(int(filtered_df[filtered_df['sales']>int(units_sold)]['sales'].sum()))

