from typing import List, Optional
from pydantic import BaseModel


class StudentInput(BaseModel):
    z_score: float
    subject_stream: str
    district: str

class DegreeProgram(BaseModel):
    degree_name: str
    subject_stream: str
    district: str
    cutoff_z_score: float
    university: Optional[str] = None

class RecommendationResponse(BaseModel):
    eligible_degrees: List[DegreeProgram]
    total_count: int
    student_input: StudentInput    
    