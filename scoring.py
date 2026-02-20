def score_resume(text, skills, grammar_feedback=None, job_role=None, missing_skills=None):

    score = 40   # Base score (lower so variation shows)
    text_lower = text.lower()

    # =========================
    # 1️⃣ Skill Strength
    # =========================
    score += len(skills) * 5

    # =========================
    # 2️⃣ Missing Skills Penalty
    # (Important for role change)
    # =========================
    if missing_skills:
        score -= len(missing_skills) * 4

    # =========================
    # 3️⃣ Resume Length Quality
    # =========================
    word_count = len(text.split())

    if word_count > 700:
        score += 15
    elif word_count > 400:
        score += 10
    elif word_count < 150:
        score -= 10

    # =========================
    # 4️⃣ Important Keywords
    # =========================
    keywords = [
        "project", "experience", "internship",
        "achievement", "certification",
        "research", "development"
    ]

    for word in keywords:
        if word in text_lower:
            score += 3

    # =========================
    # 5️⃣ Grammar Quality
    # =========================
    if grammar_feedback:
        score -= len(grammar_feedback) * 2

    # =========================
    # 6️⃣ Job Role Matching Bonus
    # =========================
    if job_role:
        role_words = job_role.lower().split()
        for word in role_words:
            if word in text_lower:
                score += 3

    # =========================
    # 7️⃣ Diversity Bonus
    # (Makes output vary more)
    # =========================
    unique_words = len(set(text_lower.split()))
    score += min(unique_words // 40, 10)

    # =========================
    # Final Clamp
    # =========================
    score = max(0, min(score, 100))

    return round(score)