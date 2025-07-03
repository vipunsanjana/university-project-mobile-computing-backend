from typing import List, Optional
from pydantic import BaseModel

class StudentInput(BaseModel):
    """
    Represents the input data provided by a student, including their Z-score,
    academic subject stream, and district information.
    """
    z_score: float
    subject_stream: str
    district: str

class DegreeProgram(BaseModel):
    """
    Represents a university degree program, including its name, required subject stream,
    district-specific cutoff Z-score, and the optional university offering it.
    """
    degree_name: str
    subject_stream: str
    district: str
    cutoff_z_score: float
    university: Optional[str] = None

class RecommendationResponse(BaseModel):
    """
    Response model containing the list of degree programs a student is eligible for,
    along with the total count and the original input used for the recommendation.
    """
    eligible_degrees: List[DegreeProgram]
    total_count: int
    student_input: StudentInput
