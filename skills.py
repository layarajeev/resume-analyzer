import spacy

nlp = spacy.load("en_core_web_sm")

# Role-based skill mapping
ROLE_SKILLS = {
    "engineer": [
        "python", "java", "c++", "sql",
        "html", "css", "javascript",
        "react", "node", "git"
    ],
    "manager": [
        "leadership", "communication",
        "project management", "teamwork",
        "strategy", "planning"
    ],
    "data": [
        "python", "machine learning",
        "data analysis", "statistics",
        "pandas", "numpy", "sql"
    ]
}


def extract_skills(text, job_role=None):

    text_lower = text.lower()
    detected = []
    missing = []

    # Detect all skills from DB
    for role in ROLE_SKILLS:
        for skill in ROLE_SKILLS[role]:
            if skill in text_lower and skill not in detected:
                detected.append(skill)

    # If job role given → check role-specific expectations
    if job_role:
        job_role_lower = job_role.lower()

        for role_key in ROLE_SKILLS:
            if role_key in job_role_lower:
                expected_skills = ROLE_SKILLS[role_key]

                for skill in expected_skills:
                    if skill not in detected:
                        missing.append(skill)

    return detected, missing