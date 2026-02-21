import requests
import json

API_KEY = "YOUR_OPENAI_API_KEY"


def analyze_resume_ai(text, job_role="", job_desc=""):

    prompt = f"""
You are a professional resume evaluator.

Job Role:
{job_role}

Job Description:
{job_desc}

Resume:
{text[:3500]}

Evaluate realistically.

Return ONLY JSON:

{{
 "score": number (0-100),
 "matched_skills": [],
 "missing_skills": [],
 "recommendations": [],
 "summary": "short evaluation"
}}

IMPORTANT:
- If resume is unrelated to job role, give low score.
- Be strict like a recruiter.
- Do not hallucinate skills.
"""

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    try:
        return json.loads(result["choices"][0]["message"]["content"])
    except:
        return {
            "score": 50,
            "matched_skills": [],
            "missing_skills": [],
            "recommendations": ["AI analysis failed"],
            "summary": "Error analyzing resume."
        }