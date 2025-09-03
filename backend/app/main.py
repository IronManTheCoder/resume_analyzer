from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
import base64
from .models import AnalyzeRequest, AnalyzeResponse, ScoreBreakdown
from .analyzer import ResumeAnalyzer

# Create FastAPI application instance
app = FastAPI(title="Resume Analyzer API", version="1.0.0")

# Initialize the analyzer
analyzer = ResumeAnalyzer()

# Configure CORS for local development
origins = [
    "http://localhost:3000",    # React dev server
    "http://127.0.0.1:3000",    # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Simple hello world endpoint to test the server"""
    return {"message": "Hello from Resume Analyzer API!"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_resume(request: AnalyzeRequest):
    """
    Analyze resume against job description and return score with recommendations.
    
    Uses the ResumeAnalyzer to perform keyword matching, format analysis,
    and length assessment to provide actionable feedback.
    """
    start_time = time.time()
    
    try:
        # Decode the base64 resume file (for now, treat as plain text)
        # TODO: Add proper PDF/DOCX parsing in next step
        try:
            resume_text = base64.b64decode(request.resume_file).decode('utf-8')
        except:
            # If it's not valid base64, treat as plain text for testing
            resume_text = request.resume_file
        
        # Run the analysis
        analysis_result = analyzer.analyze_resume(resume_text, request.job_description)
        
        # Create the response using our analysis results
        breakdown = ScoreBreakdown(
            keyword_score=analysis_result['breakdown']['keyword_score'],
            format_score=analysis_result['breakdown']['format_score'],
            length_score=analysis_result['breakdown']['length_score']
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return AnalyzeResponse(
            overall_score=analysis_result['overall_score'],
            breakdown=breakdown,
            recommendations=analysis_result['recommendations'],
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}") 