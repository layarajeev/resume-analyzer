"""Resume scoring utilities."""

from typing import List
from skills import ROLE_SKILLS


def _find_expected_skills(job_role: str) -> List[str]:
    """Return expected skills list for a given job_role using ROLE_SKILLS.
    If an exact role key isn't found, return an empty list.
    """
    if not job_role:
        return []
    jr = job_role.lower()
    for role_key, skills_list in ROLE_SKILLS.items():
        if role_key in jr:
            return skills_list
    return []


def score_resume(text: str, skills: List[str], grammar_feedback=None, job_role: str = None, missing_skills: List[str] = None) -> int:
    """Compute a 0-100 resume score.

    Scoring breakdown (approximate):
      - Role-skill match: up to 65 points
      - Keywords / experience signals: up to 15 points
      - Length & diversity: up to 10 points
      - Grammar penalty: up to -20 points
      - Missing-skills penalty: up to -20 points
      - Base floor: 20 points
    """
    if missing_skills is None:
        missing_skills = []

    text_lower = (text or "").lower()
    detected = set([s.lower() for s in (skills or [])])

    # ----- Role matching -----
    expected = _find_expected_skills(job_role or "")
    role_score = 0.0

    # Infer dominant role from resume by counting overlaps with ROLE_SKILLS
    role_counts = {}
    for role_key, role_skills in ROLE_SKILLS.items():
        role_set = set([s.lower() for s in role_skills])
        role_counts[role_key] = len(detected & role_set)
    # dominant role and confidence
    dominant_role = max(role_counts, key=lambda k: role_counts[k]) if role_counts else None
    total_role_matches = sum(role_counts.values())
    dominant_count = role_counts.get(dominant_role, 0) if dominant_role else 0
    dominant_confidence = (dominant_count / total_role_matches) if total_role_matches > 0 else 0

    if expected:
        expected_set = set([s.lower() for s in expected])
        matches = len(detected & expected_set)
        role_score = (matches / max(len(expected_set), 1)) * 65.0
    else:
        # Unknown/unsupported role key → attempt lightweight keyword match
        jr_words = [w for w in (job_role or "").lower().split() if len(w) > 2]
        if jr_words:
            matches = 0
            for w in jr_words:
                if w in text_lower or any(w in s for s in detected):
                    matches += 1
            role_score = (matches / len(jr_words)) * 60.0
        else:
            role_score = 0.0

    # ----- Keywords / experience signals -----
    keywords = [
        "project", "experience", "internship",
        "achievement", "certification", "research",
        "development", "lead", "managed", "senior",
        "junior", "engineer", "pharmac", "pharmacy"
    ]
    kw_score = 0
    for kw in keywords:
        if kw in text_lower:
            kw_score += 2
    kw_score = min(kw_score, 15)

    # ----- Length & diversity -----
    words = text.split()
    wc = len(words)
    length_score = 0
    if wc > 700:
        length_score += 5
    elif wc > 400:
        length_score += 3
    elif wc < 150:
        length_score -= 5

    unique_words = len(set(text_lower.split()))
    diversity_bonus = min(unique_words // 60, 5)

    # ----- Grammar penalty -----
    grammar_penalty = 0
    if grammar_feedback:
        try:
            grammar_penalty = min(len(grammar_feedback) * 2, 20)
        except Exception:
            grammar_penalty = 0

    # ----- Missing skills penalty (if provided) -----
    missing_penalty = 0
    if missing_skills:
        missing_penalty = min(len(missing_skills) * 3, 20)

    # ----- Domain mismatch penalty -----
    # If the resume strongly indicates one role but the requested job_role is for another domain,
    # apply a heavy penalty so cross-domain matches (engineer vs pharmacist) score low.
    domain_mismatch_penalty = 0
    if job_role and dominant_role and dominant_confidence >= 0.4:
        jr_lower = (job_role or "").lower()
        # if job_role mentions a role key (e.g., "engineer", "data") and it differs from dominant
        mentioned_role = None
        for rk in ROLE_SKILLS.keys():
            if rk in jr_lower:
                mentioned_role = rk
                break
        if mentioned_role and mentioned_role != dominant_role:
            domain_mismatch_penalty = 30
        else:
            # If job role doesn't map to known keys but resume clearly belongs to another domain,
            # penalize moderately when job role words are absent from the resume
            if not mentioned_role and dominant_confidence >= 0.6 and not any(w in text_lower for w in jr_lower.split() if len(w) > 2):
                domain_mismatch_penalty = 20

    # ----- Aggregate and clamp -----
    base = 20
    raw = base + role_score + kw_score + length_score + diversity_bonus - grammar_penalty - missing_penalty - domain_mismatch_penalty
    score = max(0, min(int(round(raw)), 100))
    return score


def resume_feedback(text: str, job_role: str = None) -> List[str]:
    """Generate simple actionable recommendations based on resume content and role.

    Important: Do not echo or include the job posting text in recommendations.
    """
    recs = []
    text_lower = (text or "").lower()

    # Encourage role-aligned skills (do not echo the job posting text)
    expected = _find_expected_skills(job_role or "")
    if expected:
        recs.append("Tailor your resume to the target role by including relevant skills such as: " + ", ".join(expected[:6]) + ".")

    # Add general suggestions
    if "project" not in text_lower:
        recs.append("Add detailed project examples with measurable outcomes.")
    if "experience" not in text_lower and "internship" not in text_lower:
        recs.append("List concrete experience items or internships relevant to the role.")
    if len(text_lower.split()) < 200:
        recs.append("Expand descriptions to better highlight achievements and responsibilities.")

    if not recs:
        recs = [
            "Add measurable achievements.",
            "Include relevant technical projects.",
            "Keep formatting consistent.",
        ]

    return recs
