from flask import Flask, request, jsonify, send_from_directory
import os
from PyPDF2 import PdfReader

# AI modules
from skills import extract_skills
from grammar import grammar_check
from scoring import score_resume

app = Flask(__name__, static_folder=".", static_url_path="")


# Serve frontend
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Resume analysis route
@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files.get("resume")
    job_role = request.form.get("job_role", "")
    job_desc = request.form.get("job_description", "")

    if not file:
        return jsonify({"message": "No file uploaded"}), 400

    text = ""

    # PDF extraction
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""

    # TXT fallback
    else:
        text = file.read().decode("utf-8", errors="ignore")

    # AI processing
    skills, missing = extract_skills(text, job_role)
    grammar = grammar_check(text)
    score = score_resume(text, skills, grammar, job_role, missing)

    # Recommendations
    recommendations = [
        "Add measurable achievements.",
        "Include relevant technical projects.",
        "Keep formatting consistent.",
        "Highlight key skills clearly."
    ]

    return jsonify({
        "score": score,
        "skills": skills,
        "missing_skills": missing,
        "grammar": grammar,
        "recommendations": recommendations,
        "summary": "AI-powered resume analysis completed."
    })


if __name__ == "__main__":
    app.run(debug=True)