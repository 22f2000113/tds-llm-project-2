import re
import subprocess

# Input string
def get_file_move_and_hash(question):
    # Regular expression to extract the string to replace and its replacement
    result = subprocess.run(
    ['bash', "./codes/w1/w1q16.sh", "./inputs/W1Q16"],capture_output=True, text=True)
    return result.stdout
