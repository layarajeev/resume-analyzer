import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Main skill database (expand anytime)
SKILL_DB = [
    "python", "java", "c", "c++", "sql",
    "machine learning", "data science",
    "html", "css", "javascript",
    "react", "node", "communication",
    "teamwork", "leadership",
    "problem solving", "git"
]


def extract_skills(text, job_role=None):
    doc = nlp(text.lower())

    detected_skills = []

    # AI-based skill detection
    for skill in SKILL_DB:
        if skill in doc.text:
            detected_skills.append(skill)

    # Optional: Missing skills for job role
    missing_skills = []
    if job_role:
        job_doc = nlp(job_role.lower())
        for skill in SKILL_DB:
            if skill in job_doc.text and skill not in detected_skills:
                missing_skills.append(skill)

    return detected_skills, missing_skills