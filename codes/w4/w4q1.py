import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def get_command(question):
    page_number = re.search(r'page number (\d+)', question)
    return_value=count_ducks_from_cricinfo(page_number)
    print('get_command',return_value)
    return int(return_value)

def count_ducks_from_cricinfo(page_number=26):
    url = f"https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;template=results;type=batting;page={page_number}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error for bad status
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return

    soup = BeautifulSoup(response.text, "lxml")
    
    # Extract the first table
    tables = pd.read_html(str(soup))
    batting_table = tables[2]
    #print(batting_table)
    if "0" not in batting_table.columns:
        print("Column for ducks ('0') not found.")
        print("Columns found:", batting_table.columns.tolist())
        return

    total_ducks = batting_table["0"].sum()
    print(f"Total number of ducks on page {page_number}: {total_ducks}")
    return total_ducks

