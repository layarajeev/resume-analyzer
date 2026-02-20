# Role-based skill mapping
ROLE_SKILLS = {
    "engineer": [
        "python", "java", "c++", "c#", "sql",
        "html", "css", "javascript",
        "react", "node", "git", "docker",
        "aws", "azure", "java", "spring",
        "restful", "api", "database"
    ],
    "manager": [
        "leadership", "communication",
        "project management", "teamwork",
        "strategy", "planning", "agile",
        "scrum", "kanban", "delegation"
    ],
    "data": [
        "python", "machine learning",
        "data analysis", "statistics",
        "pandas", "numpy", "sql", "spark",
        "tableau", "powerbi", "r programming",
        "tensorflow", "scikit-learn"
    ],
    "designer": [
        "figma", "adobe xd", "adobe photoshop",
        "illustrator", "ui design", "ux design",
        "wireframing", "prototyping", "css"
    ]
}

# All skills for general detection
ALL_SKILLS = []
for role_skills in ROLE_SKILLS.values():
    ALL_SKILLS.extend(role_skills)
ALL_SKILLS = list(set(ALL_SKILLS))


def extract_skills(text, job_role=None):
    """Extract skills from text based on role-based skill mapping."""
    if not text or len(text.strip()) < 2:
        return [], []
    
    text_lower = text.lower()
    detected = []
    missing = []

    # Detect all skills from DB
    for skill in ALL_SKILLS:
        # Match whole words with word boundaries
        if skill in text_lower and skill not in detected:
            detected.append(skill)

    # If job role given → check role-specific expectations
    if job_role and len(job_role.strip()) > 0:
        job_role_lower = job_role.lower()

        for role_key in ROLE_SKILLS:
            if role_key in job_role_lower:
                expected_skills = ROLE_SKILLS[role_key]

                for skill in expected_skills:
                    if skill not in detected:
                        missing.append(skill)
                break  # Found matching role

    return detected, missing