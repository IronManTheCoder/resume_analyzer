# System Design Document: Resume Analyzer MVP

## 1. Overview

This document outlines the system design for a simple Resume Analyzer application that allows users to upload their resume, paste a job description, and receive actionable feedback with a confidence score.

### 1.1 Design Principles
- **Simplicity First:** Minimal complexity for MVP
- **Local Development First:** Traditional server setup before cloud deployment
- **Stateless Design:** No persistent storage required
- **Single Page Application:** Streamlined user experience
- **Fast Feedback:** Results within 5-10 seconds

## 2. High-Level Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Frontend      │ ◄──────────────► │   Backend       │
│   (React)       │                 │   (FastAPI)     │
└─────────────────┘                 └─────────────────┘
                                            │
                                            ▼
                                    ┌─────────────────┐
                                    │  Analysis       │
                                    │  Engine         │
                                    │  (NLTK/Python)  │
                                    └─────────────────┘
```

### 2.1 Component Overview
- **Frontend:** Single-page React application with file upload and results display
- **Backend:** FastAPI server handling file processing and analysis
- **Analysis Engine:** Python-based text processing and scoring algorithm

## 3. Frontend Design

### 3.1 User Interface Layout
```
┌─────────────────────────────────────────────────────┐
│                 Resume Analyzer                     │
├─────────────────────────────────────────────────────┤
│  📄 Upload Resume                                   │
│  ┌─────────────────┐                               │
│  │ Drag & Drop     │  [Browse Files]               │
│  │ Area            │                               │
│  └─────────────────┘                               │
│                                                     │
│  📝 Job Description                                 │
│  ┌─────────────────────────────────────────────────┤
│  │                                                 │
│  │  Paste job description here...                  │
│  │                                                 │
│  └─────────────────────────────────────────────────┤
│                                                     │
│              [Analyze Resume]                       │
│                                                     │
│  📊 Results (appears after analysis)               │
│  ┌─────────────────────────────────────────────────┤
│  │ Score: 78/100                                   │
│  │ ┌─────┬─────┬─────┐                             │
│  │ │ 68% │ 85% │ 82% │                             │
│  │ │Keys │Fmt  │Len  │                             │
│  │ └─────┴─────┴─────┘                             │
│  │                                                 │
│  │ 💡 Recommendations:                             │
│  │ 1. Add keywords: Python, AWS, Docker           │
│  │ 2. Use bullet points in experience section     │
│  │ 3. Quantify achievements with metrics           │
│  └─────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────┘
```

### 3.2 Frontend Components

#### 3.2.1 App Component
```javascript
// Main application container
- State management for upload, job description, results
- Handles API communication
- Manages loading states
```

#### 3.2.2 FileUpload Component
```javascript
// File upload functionality
- Drag & drop support
- File validation (PDF/DOCX, max 5MB)
- Upload progress indicator
- Error handling for invalid files
```

#### 3.2.3 JobDescription Component
```javascript
// Job description input
- Textarea with character counter (max 5,000)
- Basic input validation
- Clear/reset functionality
```

#### 3.2.4 AnalyzeButton Component
```javascript
// Analysis trigger
- Disabled state when inputs incomplete
- Loading spinner during analysis
- Error handling for failed requests
```

#### 3.2.5 Results Component
```javascript
// Results display
- Overall score visualization
- Breakdown scores (Keywords, Format, Length)
- Recommendation list
- Option to analyze another resume
```

### 3.3 Frontend Technology Stack
- **Framework:** React 18
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **File Handling:** Browser File API
- **State Management:** React hooks (useState, useEffect)

## 4. Backend Design

### 4.1 API Endpoints

#### 4.1.1 POST /analyze
**Purpose:** Process resume and job description, return analysis results

**Request:**
```json
{
  "resume_file": "base64_encoded_file_content",
  "file_type": "pdf|docx",
  "job_description": "string (max 5000 chars)"
}
```

**Response:**
```json
{
  "overall_score": 78,
  "breakdown": {
    "keyword_score": 68,
    "format_score": 85,
    "length_score": 82
  },
  "recommendations": [
    "Add keywords: Python, AWS, Docker",
    "Use bullet points in experience section", 
    "Quantify achievements with metrics"
  ],
  "processing_time_ms": 1250
}
```

#### 4.1.2 GET /health
**Purpose:** Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

### 4.2 Backend Components

#### 4.2.1 Main Application (main.py)
```python
# FastAPI application setup
- CORS configuration for frontend
- Request/response models
- Error handling middleware
- File size validation
```

#### 4.2.2 File Parser (parsers.py)
```python
# Document text extraction
- PDF parsing using PyPDF2
- DOCX parsing using python-docx
- Text cleaning and normalization
- Error handling for corrupted files
```

#### 4.2.3 Analysis Engine (analyzer.py)
```python
# Core analysis logic
- Keyword extraction and matching
- Format analysis (sections, bullet points)
- Length analysis and scoring
- Recommendation generation
```

#### 4.2.4 Models (models.py)
```python
# Pydantic models for request/response
- AnalyzeRequest
- AnalyzeResponse
- ScoreBreakdown
```

## 5. Data Flow

### 5.1 End-to-End Process Flow

```
1. User uploads resume file
   ↓
2. Frontend validates file (type, size)
   ↓
3. User pastes job description
   ↓
4. Frontend sends POST /analyze request
   ↓
5. Backend receives and validates request
   ↓
6. File parser extracts text from resume
   ↓
7. Analysis engine processes resume vs job description
   ↓
8. Scoring algorithm calculates breakdown scores
   ↓
9. Recommendation engine generates suggestions
   ↓
10. Backend returns structured response
    ↓
11. Frontend displays results to user
```

### 5.2 Analysis Algorithm Flow

```
Resume Text + Job Description
         ↓
┌─────────────────────────────────┐
│     Text Preprocessing          │
│ - Remove special characters     │
│ - Convert to lowercase          │
│ - Tokenize words               │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│     Keyword Analysis (60%)      │
│ - Extract keywords from job     │
│ - Count matches in resume       │
│ - Calculate percentage match    │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│     Format Analysis (20%)       │
│ - Detect sections (headers)     │
│ - Count bullet points          │
│ - Check contact information    │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│     Length Analysis (20%)       │
│ - Word count assessment         │
│ - Optimal length comparison     │
│ - Density evaluation           │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│     Score Calculation           │
│ Final = (Keywords×0.6) +        │
│         (Format×0.2) +          │
│         (Length×0.2)            │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│     Recommendation Engine       │
│ - Generate top 3 suggestions   │
│ - Prioritize by impact         │
│ - Provide actionable advice    │
└─────────────────────────────────┘
```

## 6. Technical Specifications

### 6.1 File Processing Requirements
- **Supported Formats:** PDF, DOCX
- **Maximum File Size:** 5MB
- **Text Extraction:** PyPDF2 for PDF, python-docx for DOCX
- **Error Handling:** Graceful degradation for parsing failures

### 6.2 Analysis Engine Specifications

#### 6.2.1 Keyword Matching Algorithm
```python
def calculate_keyword_score(resume_text, job_description):
    # Extract important keywords from job description
    job_keywords = extract_keywords(job_description)
    
    # Count matches in resume
    matches = count_keyword_matches(resume_text, job_keywords)
    
    # Calculate percentage
    score = (matches / len(job_keywords)) * 100
    return min(score, 100)  # Cap at 100%
```

#### 6.2.2 Format Scoring Criteria
- **Contact Information:** 20 points
- **Professional Summary:** 15 points  
- **Work Experience Section:** 25 points
- **Education Section:** 15 points
- **Skills Section:** 15 points
- **Bullet Points Usage:** 10 points

#### 6.2.3 Length Scoring Criteria
- **Optimal Range:** 400-800 words (100% score)
- **Acceptable Range:** 300-1000 words (80% score)
- **Below/Above Range:** Linear penalty

### 6.3 Performance Requirements
- **Response Time:** < 10 seconds for analysis
- **File Upload:** < 5 seconds for 5MB file
- **Concurrent Users:** Support 10 simultaneous analyses

## 7. Local Development Architecture

### 7.1 Local Development Setup
```
┌─────────────────┐    HTTP (localhost:3000)    ┌─────────────────┐
│   Frontend      │ ◄─────────────────────────► │   Backend       │
│   React Dev     │                             │   FastAPI       │
│   Server        │    API calls to :8000       │   + Uvicorn     │
│   (port 3000)   │                             │   (port 8000)   │
└─────────────────┘                             └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                             ┌─────────────────┐
│   Hot Reload    │                             │   Python Venv   │
│   File Watcher  │                             │   Dependencies  │
└─────────────────┘                             └─────────────────┘
```

### 7.2 Local Environment Setup

#### 7.2.1 Backend Setup (Python Virtual Environment)
```bash
# Navigate to project directory
cd /Users/pgangasani/Documents/development/codebase/Resume_Analyzer

# Create backend directory and virtual environment
mkdir backend
cd backend
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install fastapi uvicorn python-multipart PyPDF2 python-docx nltk

# Create requirements.txt
pip freeze > requirements.txt
```

#### 7.2.2 Frontend Setup (Node.js)
```bash
# Navigate back to project root
cd /Users/pgangasani/Documents/development/codebase/Resume_Analyzer

# Create React frontend
npx create-react-app frontend
cd frontend

# Install additional dependencies
npm install axios tailwindcss @tailwindcss/forms

# Initialize Tailwind CSS
npx tailwindcss init
```

### 7.3 Development Workflow
- **Backend:** Run `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- **Frontend:** Run `npm start` (automatically opens localhost:3000)
- **CORS:** Configure FastAPI to allow requests from localhost:3000
- **Hot Reload:** Both servers support automatic reloading on file changes

## 8. Security Considerations

### 8.1 File Upload Security
- File type validation (MIME type checking)
- File size limits (5MB maximum)
- Virus scanning (basic validation)
- Temporary file cleanup

### 8.2 Input Validation
- Job description length limits
- Text sanitization to prevent injection
- Rate limiting on API endpoints

### 8.3 Data Privacy
- No persistent storage of uploaded files
- Files processed in memory only
- Automatic cleanup after analysis

## 9. Error Handling Strategy

### 9.1 Frontend Error Handling
- File upload errors (size, type, corruption)
- Network connectivity issues
- API timeout handling
- User-friendly error messages

### 9.2 Backend Error Handling
- File parsing failures
- Analysis engine errors
- Input validation errors
- Graceful degradation with partial results

## 10. Development Workflow

### 10.1 Local Project Structure
```
Resume_Analyzer/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── JobDescription.js
│   │   │   ├── AnalyzeButton.js
│   │   │   └── Results.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── backend/
│   ├── venv/                    # Python virtual environment
│   ├── app/
│   │   ├── main.py             # FastAPI application
│   │   ├── models.py           # Pydantic models
│   │   ├── parsers.py          # File parsing logic
│   │   └── analyzer.py         # Analysis engine
│   ├── requirements.txt
│   └── run_dev.py              # Development server script
├── Product_Requirements_Document.md
├── System_Design_Document.md
└── dev_setup.md                # Local development instructions
```

### 10.2 Local Development Environment
- **Frontend:** Node.js 18+, React development server (localhost:3000)
- **Backend:** Python 3.9+ in virtual environment (localhost:8000)
- **Development Tools:** Hot reload enabled for both frontend and backend
- **CORS:** FastAPI configured to accept requests from localhost:3000
- **File Storage:** Temporary in-memory processing, no persistent storage needed

## 11. Implementation Timeline

### Week 1 Development Schedule

| Day | Frontend Tasks | Backend Tasks |
|-----|----------------|---------------|
| 1 | Project setup, basic layout | FastAPI setup, basic endpoints |
| 2 | File upload component | PDF/DOCX parsing implementation |
| 3 | Job description input, UI polish | Analysis engine core logic |
| 4 | Results display component | Scoring algorithm implementation |
| 5 | API integration, error handling | Recommendation engine |
| 6 | Testing, responsive design | Error handling, validation |
| 7 | Deployment preparation | Production deployment |

## 12. API Contract Details

### 12.1 Request/Response Models

#### Analyze Request
```python
class AnalyzeRequest(BaseModel):
    resume_file: str  # base64 encoded
    file_type: Literal["pdf", "docx"]
    job_description: str = Field(max_length=5000)
```

#### Analyze Response
```python
class ScoreBreakdown(BaseModel):
    keyword_score: int = Field(ge=0, le=100)
    format_score: int = Field(ge=0, le=100)
    length_score: int = Field(ge=0, le=100)

class AnalyzeResponse(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    breakdown: ScoreBreakdown
    recommendations: List[str] = Field(max_items=3)
    processing_time_ms: int
```

### 12.2 Error Response Format
```python
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[str] = None
```

## 13. Monitoring and Logging

### 13.1 Basic Monitoring
- API response times
- File processing success rates
- Error frequency and types
- User interaction patterns

### 13.2 Logging Strategy
- Structured logging with timestamps
- Request/response logging (without sensitive data)
- Error stack traces for debugging
- Performance metrics

## 14. Scalability Considerations

### 14.1 Current Limitations
- In-memory processing only
- Single server deployment
- No caching layer
- Synchronous processing

### 14.2 Future Scaling Options
- Horizontal scaling with load balancer
- Async processing with task queues
- Redis caching for common analyses
- Database for user sessions (future enhancement)

## 15. Testing Strategy

### 15.1 Frontend Testing
- Component unit tests (Jest/React Testing Library)
- File upload integration tests
- User interaction flow tests
- Cross-browser compatibility

### 15.2 Backend Testing
- API endpoint tests (pytest)
- File parsing tests with sample documents
- Analysis algorithm unit tests
- Error handling validation

### 15.3 End-to-End Testing
- Complete user flow automation
- Performance testing with various file sizes
- Error scenario testing

## 16. Local Development Setup

### 16.1 Getting Started Locally

#### Step 1: Backend Setup
```bash
# Create and activate Python virtual environment
cd /Users/pgangasani/Documents/development/codebase/Resume_Analyzer
mkdir backend && cd backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install fastapi uvicorn python-multipart PyPDF2 python-docx nltk pydantic

# Save dependencies
pip freeze > requirements.txt
```

#### Step 2: Frontend Setup
```bash
# Navigate to project root and create React app
cd /Users/pgangasani/Documents/development/codebase/Resume_Analyzer
npx create-react-app frontend
cd frontend

# Install additional dependencies
npm install axios tailwindcss @tailwindcss/forms @headlessui/react

# Initialize Tailwind CSS
npx tailwindcss init -p
```

### 16.2 Running the Application Locally

#### Terminal 1 - Backend Server:
```bash
cd /Users/pgangasani/Documents/development/codebase/Resume_Analyzer/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### Terminal 2 - Frontend Server:
```bash
cd /Users/pgangasani/Documents/development/codebase/Resume_Analyzer/frontend
npm start
```

### 16.3 Local Configuration
```python
# backend/app/main.py - CORS configuration for local development
from fastapi.middleware.cors import CORSMiddleware

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
```

### 16.4 Development URLs
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (FastAPI auto-generated)

## 17. Success Metrics

### 17.1 Technical Metrics
- **Uptime:** > 99%
- **Response Time:** < 10 seconds average
- **Success Rate:** > 95% for valid inputs
- **File Processing:** > 90% success rate

### 17.2 User Experience Metrics
- **Time to Results:** < 30 seconds total
- **Error Rate:** < 5% user-facing errors
- **User Completion:** > 80% complete the full flow

## 18. Local Development Benefits

### 18.1 Advantages of Local Development
- **Full Control:** Complete control over environment and dependencies
- **Fast Iteration:** Immediate feedback with hot reload
- **Debugging:** Easy access to logs, debuggers, and development tools
- **No Cloud Costs:** Free development environment
- **Learning:** Understand the full stack without abstraction layers

### 18.2 Development Best Practices
- **Version Control:** Use Git for tracking changes
- **Environment Isolation:** Virtual environments prevent dependency conflicts
- **Code Organization:** Separate frontend and backend concerns
- **Testing:** Easy to run unit tests and integration tests locally

## 19. Future Cloud Migration Path

When ready to deploy to production:

### 19.1 Simple Cloud Options
- **Frontend:** Netlify/Vercel (drag & drop the build folder)
- **Backend:** Railway/Render (connect GitHub repo)
- **Traditional VPS:** DigitalOcean droplet with manual setup

### 19.2 Migration Steps
1. Test thoroughly in local environment
2. Create production build of frontend (`npm run build`)
3. Update CORS settings for production domain
4. Deploy backend to cloud service
5. Deploy frontend static files
6. Update API endpoints in frontend

This local-first approach ensures you understand every component before adding cloud complexity, making you a more well-rounded developer while keeping the MVP timeline achievable. 