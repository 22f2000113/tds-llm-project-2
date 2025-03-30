
import numpy as np
import re

def calculate_sum(question) :
    sequence_pattern = r"SEQUENCE\((\d+), (\d+), (\d+), (\d+)\)"
    constrain_pattern = r"ARRAY_CONSTRAIN\((.*), (\d+), (\d+)\)"
    
    # Search for the SEQUENCE part
    sequence_match = re.search(sequence_pattern, question)
    rows = int(sequence_match.group(1))
    cols = int(sequence_match.group(2))
    start_num = int(sequence_match.group(3))
    step = int(sequence_match.group(4))
    print(f"rows:{rows}, cols:{cols}, start_num:{start_num}")
    # Search for the ARRAY_CONSTRAIN part
    constrain_match = re.search(constrain_pattern, question)
    row_limit = int(constrain_match.group(2)) - 1  # 0-based index
    col_limit = int(constrain_match.group(3))    # 1-based limit, already correct
    print(f"row_limit:{row_limit}, col_limit:{col_limit}")
    # Generate the sequence with dynamic start, rows, and cols
    sequence = np.arange(start_num, rows*cols + start_num).reshape(rows, cols)

    # Get the first row and the first 10 columns
    constrained_array = sequence[row_limit, :col_limit]
    print("after ",np.sum(constrained_array))
    return {"answer":str(int(np.sum(constrained_array)))}
