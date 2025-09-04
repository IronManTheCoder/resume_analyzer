#!/usr/bin/env python3
"""
Test script for Resume Analyzer API with real files
"""

import requests
import json

# API endpoint
API_URL = "http://127.0.0.1:8000/analyze"

def test_docx_file():
    """Test with real DOCX file"""
    print("🧪 Testing DOCX file parsing...")
    
    # Read the base64 content
    with open('test_files/docx_base64.txt', 'r') as f:
        docx_base64 = f.read().strip()
    
    # Prepare request
    request_data = {
        "resume_file": docx_base64,
        "file_type": "docx",
        "job_description": "Looking for a Python developer with FastAPI and SQL experience. Must have 5+ years experience and team leadership skills."
    }
    
    try:
        # Send request
        print(f"📤 Sending request to {API_URL}")
        response = requests.post(API_URL, json=request_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ DOCX Test SUCCESSFUL!")
            print(f"📊 Overall Score: {result['overall_score']}/100")
            print(f"📈 Breakdown:")
            print(f"   • Keywords: {result['breakdown']['keyword_score']}/100")
            print(f"   • Format: {result['breakdown']['format_score']}/100") 
            print(f"   • Length: {result['breakdown']['length_score']}/100")
            print(f"⏱️  Processing Time: {result['processing_time_ms']}ms")
            print(f"💡 Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"   {i}. {rec}")
        else:
            print(f"❌ DOCX Test FAILED: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ DOCX Test ERROR: {str(e)}")

def test_pdf_file():
    """Test with real PDF file"""
    print("\n🧪 Testing PDF file parsing...")
    
    # Read the base64 content
    with open('test_files/pdf_base64.txt', 'r') as f:
        pdf_base64 = f.read().strip()
    
    # Prepare request
    request_data = {
        "resume_file": pdf_base64,
        "file_type": "pdf", 
        "job_description": "Seeking a Senior Software Developer with Python, FastAPI, and team leadership experience. Must have database optimization skills and CI/CD experience."
    }
    
    try:
        # Send request
        print(f"📤 Sending request to {API_URL}")
        response = requests.post(API_URL, json=request_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF Test SUCCESSFUL!")
            print(f"📊 Overall Score: {result['overall_score']}/100")
            print(f"📈 Breakdown:")
            print(f"   • Keywords: {result['breakdown']['keyword_score']}/100")
            print(f"   • Format: {result['breakdown']['format_score']}/100")
            print(f"   • Length: {result['breakdown']['length_score']}/100")
            print(f"⏱️  Processing Time: {result['processing_time_ms']}ms")
            print(f"💡 Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"   {i}. {rec}")
        else:
            print(f"❌ PDF Test FAILED: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ PDF Test ERROR: {str(e)}")

def check_server():
    """Check if server is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server responded with: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not reachable: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Resume Analyzer API Test")
    print("=" * 50)
    
    # Check server first
    if not check_server():
        print("\n💡 Make sure the server is running:")
        print("   source venv/bin/activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        exit(1)
    
    # Run tests
    test_docx_file()
    test_pdf_file()
    
    print("\n🎉 Testing complete!") 