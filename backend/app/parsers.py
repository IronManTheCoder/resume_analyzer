import base64
import io
from typing import Optional
import PyPDF2
from docx import Document

class FileParser:
    """Handles parsing of PDF and DOCX files to extract text content"""
    
    def __init__(self):
        print("FileParser initialized!")
    
    def parse_pdf(self, pdf_content: bytes) -> str:
        """Extract text from PDF file bytes"""
        print(f"DEBUG: Parsing PDF file ({len(pdf_content)} bytes)")
        
        try:
            # Create a file-like object from bytes
            pdf_file = io.BytesIO(pdf_content)
            
            # Create PDF reader
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += page_text + "\n"
                print(f"DEBUG: Extracted {len(page_text)} characters from page {page_num + 1}")
            
            print(f"DEBUG: Total PDF text extracted: {len(text)} characters")
            return text.strip()
            
        except Exception as e:
            print(f"DEBUG: PDF parsing failed: {str(e)}")
            raise Exception(f"Failed to parse PDF: {str(e)}")
    
    def parse_docx(self, docx_content: bytes) -> str:
        """Extract text from DOCX file bytes"""
        print(f"DEBUG: Parsing DOCX file ({len(docx_content)} bytes)")
        
        try:
            # Create a file-like object from bytes
            docx_file = io.BytesIO(docx_content)
            
            # Create Document object
            doc = Document(docx_file)
            
            # Extract text from all paragraphs
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            print(f"DEBUG: Total DOCX text extracted: {len(text)} characters")
            return text.strip()
            
        except Exception as e:
            print(f"DEBUG: DOCX parsing failed: {str(e)}")
            raise Exception(f"Failed to parse DOCX: {str(e)}")
    
    def parse_file(self, file_content: str, file_type: str) -> str:
        """
        Main parsing function that handles both PDF and DOCX
        
        Args:
            file_content: Base64 encoded file content
            file_type: Either 'pdf' or 'docx'
        
        Returns:
            Extracted text content
        """
        print(f"DEBUG: Starting file parsing for {file_type.upper()} file")
        
        try:
            # Decode base64 content to bytes
            file_bytes = base64.b64decode(file_content)
            print(f"DEBUG: Decoded {len(file_bytes)} bytes from base64")
            
            # Parse based on file type
            if file_type.lower() == 'pdf':
                return self.parse_pdf(file_bytes)
            elif file_type.lower() == 'docx':
                return self.parse_docx(file_bytes)
            else:
                raise Exception(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            print(f"DEBUG: File parsing failed: {str(e)}")
            # Fallback: try to treat as plain text
            try:
                fallback_text = base64.b64decode(file_content).decode('utf-8')
                print(f"DEBUG: Fallback to plain text successful")
                return fallback_text
            except:
                raise Exception(f"Could not parse file as {file_type} or plain text: {str(e)}") 