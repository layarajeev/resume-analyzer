def score_resume(text, skills, grammar_feedback=None, job_role=None):
    score = 50  # Base score

    text_lower = text.lower()

    # 1️⃣ Skill strength
    score += len(skills) * 4

    # 2️⃣ Resume length quality
    word_count = len(text.split())
    if word_count > 600:
        score += 15
    elif word_count > 350:
        score += 10
    elif word_count < 150:
        score -= 10

    # 3️⃣ Important resume keywords
    important_words = [
        "project", "experience", "internship",
        "achievement", "certification", "leadership"
    ]

    for word in important_words:
        if word in text_lower:
            score += 4

    # 4️⃣ Grammar penalty (AI feedback)
    if grammar_feedback:
        score -= len(grammar_feedback) * 2

    # 5️⃣ Job role matching bonus
    if job_role:
        job_words = job_role.lower().split()
        for word in job_words:
            if word in text_lower:
                score += 3

    # Final cap
    score = max(0, min(score, 100))

    return score