import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Load environment variables
load_dotenv(override=True)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Google Sheets Configuration
cred = Credentials.from_service_account_info({
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}, scopes=SCOPES)

# Google Sheet URL
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL").replace('\\n', '\n')

# Google Sheet ID
SHEET_ID = os.getenv("SHEET_ID")

# List of all required environment variables
required_vars = [
    "SHEET_ID",
    "GOOGLE_SHEET_URL",
    "TYPE",
    "PROJECT_ID",   
    "PRIVATE_KEY_ID",
    "PRIVATE_KEY",
    "CLIENT_EMAIL",
    "CLIENT_ID",
    "AUTH_URI",
    "TOKEN_URI",
    "AUTH_PROVIDER_X509_CERT_URL",
    "CLIENT_X509_CERT_URL",
    "UNIVERSE_DOMAIN"
]

# Check for missing environment variables
missing_vars = [var_name for var_name in required_vars if not os.getenv(var_name)]

if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )
