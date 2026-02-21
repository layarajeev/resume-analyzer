from flask import Flask, request, jsonify, send_from_directory
from PyPDF2 import PdfReader

# AI modules
from skills import extract_skills
from grammar import grammar_check
from scoring import score_resume, resume_feedback

app = Flask(__name__, static_folder=".", static_url_path="")


# Serve frontend
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Resume analysis route
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files.get("resume")
        job_role = request.form.get("job_role", "")
        job_desc = request.form.get("job_description", "")

        if not file:
            return jsonify({"message": "No file uploaded"}), 400

        if file.filename == "":
            return jsonify({"message": "No file selected"}), 400

        text = ""

        # ✅ FIXED PDF READING
        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        else:
            text = file.read().decode("utf-8", errors="ignore")

        if len(text.strip()) < 20:
            return jsonify({"message": "Resume unreadable or empty"}), 400

        # AI processing
        skills, missing = extract_skills(text, job_role)
        grammar = grammar_check(text)
        score = score_resume(text, skills, grammar, job_role)

        # Recommendations
        recommendations = resume_feedback(text, job_role)

        return jsonify({
            "score": score,
            "skills": skills,
            "missing_skills": missing,
            "grammar": grammar,
            "recommendations": recommendations,
            "summary": "AI analysis complete."
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)