from pydantic import BaseModel, Field
from typing import List, Literal

class AnalyzeRequest(BaseModel):
    """Request model for resume analysis endpoint"""
    resume_file: str = Field(..., description="Base64 encoded resume file content")
    file_type: Literal["pdf", "docx"] = Field(..., description="Type of the uploaded file")
    job_description: str = Field(..., max_length=5000, description="Job description text")

class ScoreBreakdown(BaseModel):
    """Breakdown of individual scoring components"""
    keyword_score: int = Field(..., ge=0, le=100, description="Keyword matching score (0-100)")
    format_score: int = Field(..., ge=0, le=100, description="Resume format score (0-100)")
    length_score: int = Field(..., ge=0, le=100, description="Resume length score (0-100)")

class AnalyzeResponse(BaseModel):
    """Response model for resume analysis endpoint"""
    overall_score: int = Field(..., ge=0, le=100, description="Overall resume score (0-100)")
    breakdown: ScoreBreakdown = Field(..., description="Detailed score breakdown")
    recommendations: List[str] = Field(..., max_items=3, description="Top 3 improvement recommendations")
    processing_time_ms: int = Field(..., description="Time taken to process the request in milliseconds")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: str = Field(None, description="Additional error details") 