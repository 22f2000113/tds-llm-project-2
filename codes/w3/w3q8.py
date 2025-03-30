import re
import json
from fastapi import HTTPException

def analyze_query(query: str):
    # Ticket Status (example: "What is the status of ticket 83742?")
    ticket_status_pattern = r"Ticket (\d+):?\s*(current\s*status|status)"
    ticket_match = re.search(ticket_status_pattern, query)
    if ticket_match:
        ticket_id = int(ticket_match.group(1))
        return {"name": "get_ticket_status", "arguments": json.dumps({"ticket_id": ticket_id})}

    # Meeting Scheduling (example: "Schedule a meeting on 2025-02-15 at 14:00 in Room A.")
    meeting_pattern = r"Schedule a meeting on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) in (Room [A-Z])"
    meeting_match = re.search(meeting_pattern, query)
    if meeting_match:
        date = meeting_match.group(1)
        time = meeting_match.group(2)
        meeting_room = meeting_match.group(3)
        return {"name": "schedule_meeting",
                "arguments": json.dumps({"date": date, "time": time, "meeting_room": meeting_room})}

    # Expense Reimbursement (example: "Show my expense balance for employee 10056.")
    expense_pattern = r"(?i)(expense.*employee\s+(\d+))"
    expense_match = re.search(expense_pattern, query)
    if expense_match:
        employee_id = int(expense_match.group(2))
        return {"name": "get_expense_balance", "arguments": json.dumps({"employee_id": employee_id})}

    # Performance Bonus Calculation (example: "Calculate performance bonus for employee 10056 for 2025.")
    bonus_pattern = r"performance bonus for employee (\d+) for (\d{4})"
    bonus_match = re.search(bonus_pattern, query)
    if bonus_match:
        employee_id = int(bonus_match.group(1))
        current_year = int(bonus_match.group(2))
        return {"name": "calculate_performance_bonus",
                "arguments": json.dumps({"employee_id": employee_id, "current_year": current_year})}

    # Office Issue Reporting (example: "Report office issue 45321 for the Facilities department.")
    issue_pattern = r"issue\s*(\d+).*?(?:department\s+(\w+)|(\w+)\s+department|for\s+(\w+))"
    issue_match = re.search(issue_pattern, query)
    if issue_match:
        print(issue_match.groups())
        issue_code = int(issue_match.group(1))
        department = issue_match.group(2) or issue_match.group(3) or issue_match.group(4)
        return {"name": "report_office_issue",
                "arguments": json.dumps({"issue_code": issue_code, "department": department})}

    # If no pattern matched
    raise HTTPException(status_code=400, detail="Query could not be understood or matched.")