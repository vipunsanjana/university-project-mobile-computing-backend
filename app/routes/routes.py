from fastapi import APIRouter, HTTPException
from typing import List

from app.models.sheet_data import DegreeProgram, RecommendationResponse, StudentInput
from app.services.sheet_service import (
    fetch_degrees_from_google_sheets,
    generate_nearby_recommendations,
    generate_recommendations,
    get_all_districts_from_sheet,
    get_all_sheet_names
)
from app.utils.constants import DISTRICT_PROXIMITY


router = APIRouter()

@router.get("/", tags=["General"])
async def root():
    return {"message": "University Degree Recommendation API"}

@router.get("/degrees", response_model=List[DegreeProgram], tags=["Degrees"])
async def get_all_degrees():
    degrees = await fetch_degrees_from_google_sheets()
    return degrees

@router.get("/streams", tags=["Filters"])
async def get_subject_streams():
    try:
        sheet_names = get_all_sheet_names()
        return {"streams": sorted(sheet_names)}
    except Exception as e:
        return {"error": str(e)}

@router.get("/districts", tags=["Filters"])
async def get_districts():
    try:
        districts = get_all_districts_from_sheet()
        return {"districts": districts}
    except Exception as e:
        return {"error": str(e)}

@router.post("/recommend", response_model=RecommendationResponse, tags=["Recommendation"])
async def get_recommendations(student_input: StudentInput):
    try:
        return await generate_recommendations(student_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.post("/recommend-nearby", tags=["Recommendation"])
async def get_nearby_recommendations(student_input: StudentInput):
    try:
        return await generate_nearby_recommendations(student_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating nearby recommendations: {str(e)}")
    