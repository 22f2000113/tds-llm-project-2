import pandas as pd
import re


def extract_unicode_symbols(question_text):
    # Regex pattern to match any character that is not in the ASCII range (not in the range of \x00 to \x7F)
    pattern = r'[^\x00-\x7F]+'

    # Find all matches in the question text
    unicode_symbols = re.findall(pattern, question_text)

    # Combine all found Unicode characters into a single string
    # This can be further processed if needed (e.g., splitting into individual symbols)
    return unicode_symbols

def extract_matching_symbols_dynamic(question_text):
    # Regex pattern to match symbols separated by " OR " (handling optional spaces)
    pattern = r'([^\w\s]+(?:\s?OR\s?[^\w\s]+)*)'

    # Find all matches in the question text
    matches = re.findall(pattern, question_text)

    # Now clean up the matches, split them by "OR" and remove extra spaces
    symbols = set()
    for match in matches:
        # Split by "OR", strip whitespace, and add to the set (to avoid duplicates)
        symbols.update(symbol.strip() for symbol in match.split('OR'))

    return symbols

def extract_files_info_from_text(text):
    # Regular expression to find file information in the format 'filename: description with encoding'
    file_pattern = r'([a-zA-Z0-9\-_\.]+):.*?encoded in (\w+-\w+)'  # Matches the file name and encoding
    matches = re.findall(file_pattern, text)
    return [(match[0], match[1]) for match in matches]

# Helper function to sum values from a CSV file (with given encoding)
def sum_values_from_csv(file_name,encoding,symbols):
    file_path = "./inputs/W1Q12/" + file_name
    with open(file_path, encoding=encoding, errors='replace') as file:
        df1 = pd.read_csv(file)

    total_value = df1[df1['symbol'].isin(symbols)]['value'].sum()
    return total_value

def sum_utf16_values_from_csv(file_name, encoding,symbols):
    file_path = "./inputs/W1Q12/"+file_name
    df2 = pd.read_csv(file_path, sep='\t', encoding=encoding)
    total_value = df2[df2['symbol'].isin(symbols)]['value'].sum()
    return total_value

def sum_of_symbols(question):
   symbols = extract_unicode_symbols(question)
   files_encoding = extract_files_info_from_text(question)
   print(files_encoding)
   total_sum = 0
   for file_name, encoding in files_encoding:
       if encoding == 'CP-1252':
           total_sum += sum_values_from_csv(file_name,'Windows-1252',symbols)
       elif encoding == 'UTF-16':
           total_sum += sum_utf16_values_from_csv(file_name, encoding,symbols)
       else :
           total_sum += sum_values_from_csv(file_name, encoding,symbols)
   return str(int(total_sum))
