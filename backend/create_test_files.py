#!/usr/bin/env python3
"""
Script to create test PDF and DOCX files for testing our file parsing
"""

import base64
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io

def create_test_docx():
    """Create a test DOCX file"""
    print("Creating test DOCX file...")
    
    # Read our sample resume text
    with open('test_files/sample_resume.txt', 'r') as f:
        resume_text = f.read()
    
    # Create DOCX document
    doc = Document()
    
    # Add content paragraph by paragraph
    for line in resume_text.split('\n'):
        if line.strip():
            doc.add_paragraph(line)
    
    # Save the document
    doc.save('test_files/sample_resume.docx')
    print("✅ Created test_files/sample_resume.docx")

def create_test_pdf_simple():
    """Create a simple test PDF file using reportlab"""
    print("Creating test PDF file...")
    
    try:
        # Read our sample resume text
        with open('test_files/sample_resume.txt', 'r') as f:
            resume_text = f.read()
        
        # Create PDF in memory first
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add content
        for line in resume_text.split('\n'):
            if line.strip():
                para = Paragraph(line, styles['Normal'])
                story.append(para)
                story.append(Spacer(1, 12))
        
        doc.build(story)
        
        # Save to file
        with open('test_files/sample_resume.pdf', 'wb') as f:
            f.write(buffer.getvalue())
        
        print("✅ Created test_files/sample_resume.pdf")
        
    except ImportError:
        print("❌ reportlab not installed. Let's create a simpler PDF test...")
        create_simple_text_pdf()

def create_simple_text_pdf():
    """Create a very simple PDF using basic canvas"""
    print("Creating simple PDF with canvas...")
    
    # Read our sample resume text
    with open('test_files/sample_resume.txt', 'r') as f:
        resume_text = f.read()
    
    # Create simple PDF
    c = canvas.Canvas('test_files/sample_resume.pdf', pagesize=letter)
    
    # Add text line by line
    y_position = 750
    for line in resume_text.split('\n')[:30]:  # Limit lines to fit on page
        if line.strip():
            c.drawString(50, y_position, line[:80])  # Limit line length
            y_position -= 20
            if y_position < 50:  # Start new page if needed
                c.showPage()
                y_position = 750
    
    c.save()
    print("✅ Created test_files/sample_resume.pdf")

def convert_to_base64(file_path):
    """Convert file to base64 for API testing"""
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    base64_content = base64.b64encode(file_content).decode('utf-8')
    print(f"Base64 length: {len(base64_content)} characters")
    return base64_content

if __name__ == "__main__":
    print("Creating test files for Resume Analyzer...")
    
    # Create test files
    create_test_docx()
    create_test_pdf_simple()
    
    print("\nConverting to base64 for API testing...")
    
    # Convert to base64 for testing
    try:
        docx_base64 = convert_to_base64('test_files/sample_resume.docx')
        print(f"DOCX base64 (first 100 chars): {docx_base64[:100]}...")
        
        # Save base64 for easy copy-paste
        with open('test_files/docx_base64.txt', 'w') as f:
            f.write(docx_base64)
        print("✅ Saved DOCX base64 to test_files/docx_base64.txt")
        
    except Exception as e:
        print(f"Error with DOCX: {e}")
    
    try:
        pdf_base64 = convert_to_base64('test_files/sample_resume.pdf')
        print(f"PDF base64 (first 100 chars): {pdf_base64[:100]}...")
        
        # Save base64 for easy copy-paste  
        with open('test_files/pdf_base64.txt', 'w') as f:
            f.write(pdf_base64)
        print("✅ Saved PDF base64 to test_files/pdf_base64.txt")
        
    except Exception as e:
        print(f"Error with PDF: {e}")
    
    print("\n🎉 Test files created! You can now test real file parsing.") 