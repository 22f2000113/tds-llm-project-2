import re
import numpy as np

pattern = r"SORTBY\(\{([0-9,]+)\},\s*\{([0-9,]+)\}\),\s*(\d+),\s*(\d+)\)"

# Using re.search to find the match
def calculate_sum(question):
    # Regular expression to extract SEQUENCE and ARRAY_CONSTRAIN parameters
    pattern = r"SORTBY\(\{([0-9,]+)\},\s*\{([0-9,]+)\}\),\s*(\d+),\s*(\d+)\)"

    # Using re.search to find the match
    match = re.search(pattern, question)

    # If a match is found, extract the groups

    if match:
        list_1 = match.group(1)  # The first list
        list_2 = match.group(2)  # The second list
        param_1 = int(match.group(3))  # First parameter (1)
        param_2 = int(match.group(4))  # Second parameter (5)
        print(f"list1:{list_1}, list_2:{list_2}, param_1:{param_1},param_2:{param_2}")
        # Convert the lists from comma-separated strings to actual Python lists
        list_1 = list(map(int, list_1.split(',')))
        list_2 = list(map(int, list_2.split(',')))

        sorted_array = [x for _, x in sorted(zip(list_2, list_1))]

        # Take the first 5 values
        values = sorted_array[param_1-1:param_2]
        return {"answer":str(int(np.sum(values)))}