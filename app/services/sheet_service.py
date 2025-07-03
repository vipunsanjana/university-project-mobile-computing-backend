import gspread
from app.models.sheet_data import DegreeProgram, RecommendationResponse, StudentInput
from app.utils import config, constants
import pandas as pd
import re
from typing import List

def initialize_google_sheet(sheet_number: int = 0):
    """
    Initializes the Google Sheets client with the service account credentials.
    Returns the first worksheet.
    """
    try:
        sheet_id = config.SHEET_ID
        client = gspread.authorize(config.cred)
        workbook = client.open_by_key(sheet_id)
        sheet = workbook.worksheets()[sheet_number]  
        constants.LOGGER.info("Google Sheets initialized successfully")
        return sheet
    except Exception as e:
        constants.LOGGER.error(f"Error initializing Google Sheets: {e}")
        raise Exception(f"Error initializing Google Sheets: {e}")

def extract_degree_and_uni(raw):
    """
    Extract degree name and university from string like 'Medicine (University of Colombo)'
    """
    if not isinstance(raw, str) or raw.strip() == "":
        return "", None

    match = re.match(r"^(.*?)\s*\((.*?)\)$", raw.strip(), re.DOTALL)
    if match:
        degree = match.group(1).replace("\n", " ").strip()
        university = match.group(2).strip()
        return degree, university
    else:
        return raw.strip(), None
    
def get_all_sheet_names():
    """
    Returns a list of all worksheet names in the Google Sheet.
    """
    try:
        sheet_id = config.SHEET_ID
        client = gspread.authorize(config.cred)
        workbook = client.open_by_key(sheet_id)
        sheet_titles = [sheet.title for sheet in workbook.worksheets()]
        constants.LOGGER.info(f"Retrieved {len(sheet_titles)} sheet(s): {sheet_titles}")
        return sheet_titles
    except Exception as e:
        constants.LOGGER.error(f"Error fetching sheet names: {e}")
        raise Exception(f"Error fetching sheet names: {e}")

def get_all_districts_from_sheet(sheet_number: int = 0) -> List[str]:
    """
    Extracts all unique districts from the given sheet index.
    """
    try:
        sheet = initialize_google_sheet(sheet_number)
        data = sheet.get_all_values()

        # Convert to DataFrame and clean up
        df = pd.DataFrame(data)
        header_index = 3
        df.columns = data[header_index]
        df = df.iloc[header_index + 1 :].reset_index(drop=True)
        df = df.loc[:, df.columns.notna()]
        df = df.loc[:, df.columns.str.strip() != ""]

        # Rename and normalize district column
        df.rename(columns={df.columns[0]: "district"}, inplace=True)
        df["district"] = df["district"].str.strip().str.title()

        # Get unique districts
        unique_districts = df["district"].dropna().unique()
        return sorted(unique_districts)

    except Exception as e:
        constants.LOGGER.error(f"Error fetching districts from sheet {sheet_number}: {e}")
        raise

async def fetch_degrees_from_google_sheets(sheet_number: int = 0) -> List[DegreeProgram]:
    """
    Fetches degree programs from the specified Google Sheet and returns a list of DegreeProgram objects.
    param sheet_number: Index of the sheet to fetch data from (0 for Bio Science, 1 for Physical Science, 2 for Technology).
    """
    try:
        sheet = initialize_google_sheet(sheet_number)
        data = sheet.get_all_values()

        # Based on your sheet, headers appear to be at row 3 (index 3)
        header_index = 3

        # Create DataFrame
        df = pd.DataFrame(data)

        # Set columns to header row
        df.columns = data[header_index]

        # Keep data only after header row
        df = df.iloc[header_index + 1 :].reset_index(drop=True)

        # Drop columns with empty or NaN headers
        df = df.loc[:, df.columns.notna()]
        df = df.loc[:, df.columns.str.strip() != ""]

        # Rename first column to 'district'
        df.rename(columns={df.columns[0]: "district"}, inplace=True)

        # Reshape data from wide to long format
        reshaped = df.melt(id_vars=["district"], var_name="raw_column", value_name="cutoff_z_score")

        # Filter rows where cutoff_z_score is numeric
        reshaped = reshaped[pd.to_numeric(reshaped["cutoff_z_score"], errors="coerce").notnull()]
        reshaped["cutoff_z_score"] = reshaped["cutoff_z_score"].astype(float)

        # Clean district names
        reshaped["district"] = reshaped["district"].str.strip().str.title()

        # Extract degree name and university from raw_column
        reshaped[["degree_name", "university"]] = reshaped["raw_column"].apply(
            lambda x: pd.Series(extract_degree_and_uni(x))
        )

        stream = "Bio Science"  

        if sheet_number == 1:
            stream = "Physical Science"
        elif sheet_number == 2:
            stream = "Technology"    

        # Build DegreeProgram list
        degrees = [
            DegreeProgram(
                degree_name=row["degree_name"],
                subject_stream=stream, 
                district=row["district"],
                cutoff_z_score=row["cutoff_z_score"],
                university=row["university"]
            )
            for _, row in reshaped.iterrows()
        ]

        return degrees

    except Exception as e:
        constants.LOGGER.error(f"Error fetching degrees from Google Sheets: {e}")
        raise

async def generate_recommendations(student_input: StudentInput) -> RecommendationResponse:
    """
    Generates degree recommendations based on the student's input.
    Filters degrees based on subject stream, district, and Z-score.
    param student_input: The input data provided by the student.
    Returns a RecommendationResponse containing eligible degrees.
    """

    sheet_number = 0
    if student_input.subject_stream == "Bio Science":
        sheet_number = 0
    elif student_input.subject_stream == "Physical Science":
        sheet_number = 1
    elif student_input.subject_stream == "Technology":
        sheet_number = 2

    degrees = await fetch_degrees_from_google_sheets(sheet_number)
    eligible_degrees = [
        degree for degree in degrees
        if degree.subject_stream.lower() == student_input.subject_stream.lower()
        and degree.district.lower() == student_input.district.lower()
        and student_input.z_score >= degree.cutoff_z_score
    ]
    eligible_degrees.sort(key=lambda x: x.cutoff_z_score)

    return RecommendationResponse(
        eligible_degrees=eligible_degrees,
        total_count=len(eligible_degrees),
        student_input=student_input
    )

async def generate_nearby_recommendations(student_input: StudentInput) -> dict:
    """
    Generates degree recommendations for the student's district and nearby districts.
    Filters degrees based on subject stream, district, and Z-score.
    param student_input: The input data provided by the student.
    Returns a dictionary containing eligible degrees in the primary district and nearby districts.
    """

    sheet_number = 0
    if student_input.subject_stream == "Bio Science":
        sheet_number = 0
    elif student_input.subject_stream == "Physical Science":
        sheet_number = 1
    elif student_input.subject_stream == "Technology":
        sheet_number = 2

    degrees = await fetch_degrees_from_google_sheets(sheet_number)
    nearby_districts = constants.DISTRICT_PROXIMITY.get(student_input.district, [])

    if not nearby_districts:
        raise ValueError("Invalid district provided.")

    eligible_degrees = []
    nearby_degrees = []

    for degree in degrees:
        if degree.subject_stream.lower() != student_input.subject_stream.lower():
            continue
        if student_input.z_score < degree.cutoff_z_score:
            continue

        if degree.district.lower() == student_input.district.lower():
            eligible_degrees.append(degree)
        elif degree.district.lower() in nearby_districts:
            nearby_degrees.append(degree)

    eligible_degrees.sort(key=lambda x: x.cutoff_z_score)
    nearby_degrees.sort(key=lambda x: x.cutoff_z_score)

    return {
        "primary_district": {
            "district": student_input.district,
            "degrees": eligible_degrees,
            "count": len(eligible_degrees)
        },
        "nearby_districts": {
            "districts": nearby_districts,
            "degrees": nearby_degrees,
            "count": len(nearby_degrees)
        },
        "student_input": student_input
    }
