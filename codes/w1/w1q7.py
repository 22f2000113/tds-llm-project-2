import re
from datetime import datetime, timedelta

week_days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

# Function to extract dates using regex
def extract_dates(text):
    # Regex pattern to extract dates in the format YYYY-MM-DD
    pattern = r'(\d{4}-\d{2}-\d{2})'
    dates = re.findall(pattern, text)
    return dates[0], dates[1]

def extract_day(text):
    pattern = r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
    day =  re.findall(pattern, text)
    return day

# Function to count Wednesdays in the date range
def count_days(start_date, end_date,day):
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize the count of Wednesdays
    count = 0

    # Iterate through each day in the date range
    current_date = start
    while current_date <= end:
        if current_date.weekday() == week_days[day]:  # 2 represents Wednesday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
            count += 1
        current_date += timedelta(days=1)
    return count


def get_date_count(question):
    # Extract start and end dates using regex
    start_date, end_date = extract_dates(question)
    day = extract_day(question)
    print(f"dates {start_date} {end_date} day {day}")
    return  str(int(count_days(start_date,end_date,day[0])))

