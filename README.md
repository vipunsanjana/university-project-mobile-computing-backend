# 🎓 University Degree Recommendation API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

> **A real-time degree recommendation system for Sri Lankan A/L students**  
> Developed by **Vipun Sajana**, Intern Software Engineer at SO2 Cloud Security Operations Center

A high-performance backend API that helps Sri Lankan A/L students discover university degree programs they qualify for based on their Z-score, subject stream, and district. Dynamically fetches and processes data from Google Sheets to provide real-time recommendations.

## 🌟 Key Features
- **Live Google Sheets Integration** - Real-time data fetching from Google Sheets
- **Smart Filtering** - Finds matching degrees based on Z-score, stream, and district
- **Nearby Districts** - Optionally includes recommendations from adjacent districts
- **CORS Enabled** - Seamless integration with Angular/React frontends
- **Docker Support** - Production-ready containerization
- **Swagger UI** - Interactive API documentation at `/docs`
- **Health Checks** - Monitoring endpoint at `/health`
- **Caching** - Reduces Google Sheets API calls
- **Error Handling** - Comprehensive error responses
- **Logging** - Structured application logging
- **Config Management** - Environment-based configuration

## 👨‍💻 Developer
**Vipun Sajana**  
Intern Software Engineer  
WSO2 Cloud Security Operations Center  

## 🛠 Technologies Used
- **Core Framework**: FastAPI 0.110+
- **Python**: 3.10+
- **Data Processing**: Pandas 2.2+
- **Google Sheets**: gspread 6.0+
- **Authentication**: Google OAuth2 Service Account
- **Web Server**: Uvicorn 0.29+
- **Containerization**: Docker 24.0+
- **Testing**: Pytest 8.0+
- **Environment**: python-dotenv 1.0+
