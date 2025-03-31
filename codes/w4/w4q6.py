import requests
import xml.etree.ElementTree as ET
import re
import json

def get_command(question):
    pattern = r'minimum of (\d+) points'
    # Search for the pattern
    match = re.search(pattern, question)

    points = match.group(1)
    return_value=get_latest_quantum_computing_post(points)
    return return_value


def get_latest_quantum_computing_post(min_points=52):
    # Use the min_points parameter in the API URL
    url = f"https://hnrss.org/newest?q=Quantum+Computing&points={min_points}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve data")
        return None

    # Parse XML response
    root = ET.fromstring(response.content)

    for item in root.findall(".//item"):
        title = item.find("title").text.strip()
        link = item.find("link").text.strip()
        description = item.find("description").text

        # Extract "Points: N" using regex
        match = re.search(r"Points:\s*(\d+)", description)
        if match:
            points = int(match.group(1))
            print("title:", title, "| points:", points)
            if points >= min_points:
                return link

    return None


