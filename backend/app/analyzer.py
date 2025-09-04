import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from typing import List, Tuple, Dict
import string

# Download required NLTK data (only happens once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResumeAnalyzer:
    """Core analysis engine for resume scoring and recommendations"""
    
    def __init__(self):
        """Initialize the analyzer"""
        print("ResumeAnalyzer initialized!")
        
    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        """
        Main analysis function - this is what gets called from our API
        We'll build this step by step
        """
        print(f"DEBUG: Starting analysis...")
        print(f"DEBUG: Resume text length: {len(resume_text)} characters")
        print(f"DEBUG: Job description length: {len(job_description)} characters")
        
        # Step 1: Calculate keyword score using our new method
        keyword_score, missing_keywords = self.calculate_keyword_score(resume_text, job_description)
        
        # Step 2: Calculate format score using our new method
        format_score, format_issues = self.calculate_format_score(resume_text)
        
        # Step 3: Calculate length score using our new method
        length_score, length_issues = self.calculate_length_score(resume_text)
        
        # Step 3: Calculate overall weighted score (60% keywords, 20% format, 20% length)
        overall_score = int(
            keyword_score * 0.6 +
            format_score * 0.2 + 
            length_score * 0.2
        )
        
        print(f"DEBUG: Final scores - Overall: {overall_score}, Keywords: {keyword_score}")
        
        # Step 4: Generate simple recommendations
        recommendations = []
        if missing_keywords:
            recommendations.append(f"Add keywords: {', '.join(missing_keywords[:3])}")
        recommendations.append("Format analysis - coming next")
        recommendations.append("Length analysis - coming after that")
        
        return {
            'overall_score': overall_score,
            'breakdown': {
                'keyword_score': keyword_score,
                'format_score': format_score,
                'length_score': length_score
            },
            'recommendations': recommendations[:3]
        }
    
    # TODO: We'll implement these methods one by one
    def calculate_keyword_score(self, resume_text: str, job_description: str) -> Tuple[int, List[str]]:
        """Calculate how well resume keywords match job description"""
        
        # Step 1: Extract important words from job description
        # Convert to lowercase and split into words
        job_words = job_description.lower().split()
        
        # Step 2: Remove common words that don't matter for matching
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                       'experience', 'work', 'working', 'job', 'position', 'role', 'candidate', 'team', 'looking'}
        
        # Step 3: Keep only meaningful keywords (longer than 2 characters, not common words)
        job_keywords = []
        for word in job_words:
            # Clean the word (remove punctuation)
            clean_word = word.strip('.,!?;:"()[]{}')
            if len(clean_word) > 2 and clean_word not in common_words:
                job_keywords.append(clean_word)
        
        # Step 4: Remove duplicates but keep the list
        unique_keywords = list(set(job_keywords))
        
        print(f"DEBUG: Found {len(unique_keywords)} keywords in job description: {unique_keywords[:10]}")
        
        # Step 5: Check how many of these keywords appear in the resume
        resume_lower = resume_text.lower()
        matched_keywords = []
        
        for keyword in unique_keywords:
            if keyword in resume_lower:
                matched_keywords.append(keyword)
        
        print(f"DEBUG: Matched {len(matched_keywords)} keywords: {matched_keywords[:10]}")
        
        # Step 6: Calculate score as percentage
        if len(unique_keywords) == 0:
            score = 50  # Default score if no keywords found
        else:
            match_percentage = len(matched_keywords) / len(unique_keywords)
            score = int(match_percentage * 100)
        
        # Step 7: Find missing keywords for recommendations
        missing_keywords = [kw for kw in unique_keywords if kw not in matched_keywords]
        
        print(f"DEBUG: Keyword score: {score}%, Missing: {missing_keywords[:5]}")
        
        return score, missing_keywords[:5]  # Return top 5 missing keywords
    
    def calculate_format_score(self, resume_text: str) -> Tuple[int, List[str]]:
        """Check resume format and structure"""
        print(f"DEBUG: Starting format analysis...")
        
        format_issues = []
        score = 0
        
        # Step 1: Check for EMAIL ADDRESS (20 points)
        # This regex pattern looks for email format: something@something.com
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        if re.search(email_pattern, resume_text):
            score += 20
            print(f"DEBUG: ✅ Email found - +20 points")
        else:
            format_issues.append("Add email address")
            print(f"DEBUG: ❌ No email found - missing 20 points")
        
        # Step 2: Check for PHONE NUMBER (10 points)  
        # This pattern looks for phone formats like: 555-123-4567, (555) 123-4567, etc.
        # Made more flexible to handle spaces and various separators
        phone_pattern = r'(\d{3}[-.\s]*\d{3}[-.\s]*\d{4}|\(\d{3}\)\s*\d{3}[-.\s]*\d{4})'
        
        if re.search(phone_pattern, resume_text):
            score += 10
            print(f"DEBUG: ✅ Phone found - +10 points")
        else:
            format_issues.append("Add phone number")
            print(f"DEBUG: ❌ No phone found - missing 10 points")
        
        # Step 3: Check for PROFESSIONAL SECTIONS (40 points total - 10 points each)
        # Define what words indicate each section
        sections = {
            'experience': ['experience', 'employment', 'work history', 'professional experience'],
            'education': ['education', 'academic', 'degree', 'university', 'college'],
            'skills': ['skills', 'technical skills', 'competencies', 'technologies'],
            'summary': ['summary', 'profile', 'objective', 'about']
        }
        
        text_lower = resume_text.lower()
        
        for section_name, section_keywords in sections.items():
            # Looks for ANY of the keywords for each section
            if any(keyword in text_lower for keyword in section_keywords):
                score += 10  # Award points for this section
                print(f"DEBUG: ✅ {section_name.title()} section found - +10 points")
            else:
                format_issues.append(f"Add {section_name} section")
                print(f"DEBUG: ❌ {section_name.title()} section missing - missing 10 points")
        
        # Step 4: Check for BULLET POINTS (20 points)
        # Look for common bullet point characters
        bullet_patterns = ['•', '▪', '‣', '⁃', '*', '-', '>', '→']
        bullet_count = 0
        
        for pattern in bullet_patterns:
            # Count how many times each bullet pattern appears
            if pattern == '-':
                # For dash, make sure it's at start of line (not just any dash)
                bullet_count += len(re.findall(r'^[-]\s', resume_text, re.MULTILINE))
            else:
                bullet_count += resume_text.count(pattern)
        
        if bullet_count >= 5:
            score += 20
            print(f"DEBUG: ✅ Good bullet usage ({bullet_count} bullets) - +20 points")
        elif bullet_count >= 2:
            score += 10
            print(f"DEBUG: ⚠️ Some bullets found ({bullet_count} bullets) - +10 points")
        else:
            format_issues.append("Use bullet points to list achievements")
            print(f"DEBUG: ❌ No bullet points found - missing 20 points")
        
        # Step 5: Check for QUANTIFIED ACHIEVEMENTS (10 points)
        # Look for numbers, percentages, dollar amounts, etc.
        number_patterns = [r'\d+%', r'\$\d+', r'\d+\+', r'\d+k', r'\d+m', r'\d+ years?', r'\d+ months?']
        quantified_count = 0
        
        for pattern in number_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            quantified_count += len(matches)
            if matches:
                print(f"DEBUG: Found quantified achievements: {matches}")
        
        if quantified_count >= 3:
            score += 10
            print(f"DEBUG: ✅ Good quantification ({quantified_count} metrics) - +10 points")
        else:
            format_issues.append("Include quantified achievements (numbers, percentages, metrics)")
            print(f"DEBUG: ❌ Not enough quantified achievements ({quantified_count} found) - missing 10 points")
        
        print(f"DEBUG: Final format score: {score}/100")
        print(f"DEBUG: Format issues: {format_issues}")
        
        return min(score, 100), format_issues
    
    def calculate_length_score(self, resume_text: str) -> Tuple[int, List[str]]:
        """Check if resume length is optimal"""
        print(f"DEBUG: Starting length analysis...")
        
        # Count words in the resume
        words = resume_text.split()
        word_count = len(words)
        
        print(f"DEBUG: Resume has {word_count} words")
        
        length_issues = []
        
        # Scoring based on word count ranges
        if 400 <= word_count <= 800:
            # Optimal range - full points
            score = 100
            print(f"DEBUG: ✅ Perfect length ({word_count} words) - +100 points")
        elif 300 <= word_count <= 1000:
            # Acceptable range - good points
            score = 80
            print(f"DEBUG: ✅ Good length ({word_count} words) - +80 points")
        elif word_count < 300:
            # Too short - scaled scoring
            score = max(20, int((word_count / 300) * 80))
            length_issues.append(f"Resume is too short ({word_count} words). Aim for 400-800 words.")
            print(f"DEBUG: ⚠️ Resume too short ({word_count} words) - +{score} points")
        else:  # word_count > 1000
            # Too long - penalty scoring
            score = max(20, int(100 - ((word_count - 800) / 10)))
            length_issues.append(f"Resume is too long ({word_count} words). Aim for 400-800 words.")
            print(f"DEBUG: ⚠️ Resume too long ({word_count} words) - +{score} points")
        
        print(f"DEBUG: Length score: {score}/100")
        print(f"DEBUG: Length issues: {length_issues}")
        
        return min(score, 100), length_issues 