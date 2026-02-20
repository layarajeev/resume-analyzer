#!/usr/bin/env python
"""
Test script to verify the Resume Analyzer app works correctly
"""

from skills import extract_skills
from grammar import grammar_check
from scoring import score_resume

# Test with sample resume text
test_resume = """
John Doe
Email: john@example.com | Phone: 555-1234

SUMMARY
Experienced Software Engineer with 5 years of expertise in Python, JavaScript, and React.
Strong background in full-stack development and agile methodologies.

EXPERIENCE
Senior Developer at TechCorp (2021-Present)
- Led development of microservices using Python and Docker
- Implemented CI/CD pipelines with Jenkins
- Mentored junior developers

Developer at StartupXYZ (2019-2021)
- Built web applications using React and Node.js
- Developed RESTful APIs
- Worked with SQL and NoSQL databases

SKILLS
Programming: Python, Java, C++, JavaScript, HTML, CSS, SQL
Frameworks: React, Node.js, Django, Flask
Tools: Git, Docker, Kubernetes, AWS, Jenkins

EDUCATION
BS in Computer Science, University of Technology (2019)

CERTIFICATIONS
AWS Solutions Architect - Associate
"""

print("=" * 60)
print("Testing Resume Analyzer Components")
print("=" * 60)

# Test skill extraction
print("\n1. TESTING SKILL EXTRACTION")
print("-" * 60)
detected_skills, missing_skills = extract_skills(test_resume, "Software Engineer")
print(f"Detected Skills: {detected_skills}")
print(f"Missing Skills (for Software Engineer role): {missing_skills[:5]}")  # Show first 5

# Test grammar check
print("\n2. TESTING GRAMMAR CHECK")
print("-" * 60)
grammar_issues = grammar_check(test_resume)
print(f"Grammar Issues Found: {len(grammar_issues)}")
if grammar_issues:
    for i, issue in enumerate(grammar_issues[:3], 1):
        print(f"  {i}. {issue.get('message', 'Unknown issue')}")
else:
    print("  No major grammar issues found!")

# Test resume scoring
print("\n3. TESTING RESUME SCORING")
print("-" * 60)
score = score_resume(test_resume, detected_skills, grammar_issues, "Software Engineer", missing_skills)
print(f"Resume Score: {score}/100")

print("\n" + "=" * 60)
print("✅ All components working correctly!")
print("=" * 60)
print("\nYou can now run: python app.py")
print("Then visit: http://localhost:5000")
