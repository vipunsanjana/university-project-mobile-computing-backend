fastapi_gsheets_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry point
│   ├── api/                 # Route definitions
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/            # Logic to interact with Google Sheets
│   │   ├── __init__.py
│   │   └── sheets_service.py
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   └── sheet_models.py
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt
├── README.md
└── venv/                    # Virtual environment
