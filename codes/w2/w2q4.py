import hashlib
import requests
from google.auth.transport.requests import Request
from google.oauth2 import credentials

# Replace with your credentials.json file path
credentials_file = "path_to_your_credentials.json"

# Load your credentials
creds = credentials.Credentials.from_authorized_user_file(credentials_file, scopes=["https://www.googleapis.com/auth/userinfo.email"])

# Refresh credentials if necessary
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

# Get the token
token = creds.token

# Get user info
response = requests.get(
    "https://www.googleapis.com/oauth2/v1/userinfo",
    params={"alt": "json"},
    headers={"Authorization": f"Bearer {token}"}
)

# Get the email address
email = response.json()["email"]

# Create a hash from email and token expiry year
hash_result = hashlib.sha256(f"{email} {creds.expiry.year}".encode()).hexdigest()[-5:]

print(hash_result)
