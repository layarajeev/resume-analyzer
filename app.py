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
    try:
        return send_from_directory(".", "index.html")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

        # PDF extraction
        try:
            if file.filename.endswith(".pdf"):
                reader = PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            else:
                # TXT and other text formats
                text = file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            return jsonify({"message": f"Error reading file: {str(e)}"}), 400

        if not text or len(text.strip()) < 10:
            return jsonify({"message": "Resume appears to be empty or unreadable"}), 400

        # AI processing
        try:
            skills, missing = extract_skills(text, job_role)
            grammar = grammar_check(text)
            score = score_resume(text, skills, grammar, job_role, missing)
        except Exception as e:
            return jsonify({"message": f"Error processing resume: {str(e)}"}), 500

        # Recommendations based on analysis
        recommendations = []
        if len(skills) < 5:
            recommendations.append("Add more technical skills to your resume.")
        if len(grammar) > 5:
            recommendations.append("Review grammar and spelling throughout.")
        if len(missing) > 0:
            recommendations.append(f"Consider adding missing skills: {', '.join(missing[:3])}")
        if len(text.split()) < 400:
            recommendations.append("Expand your resume with more details and achievements.")
        
        if not recommendations:
            recommendations = [
                "Add measurable achievements.",
                "Include relevant technical projects.",
                "Keep formatting consistent.",
                "Highlight key skills clearly."
            ]

        return jsonify({
            "score": score,
            "skills": skills if skills else [],
            "missing_skills": missing if missing else [],
            "grammar": grammar if grammar else [],
            "recommendations": recommendations,
            "summary": "AI-powered resume analysis completed."
        })
    
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    port = 3000
    app.run(debug=True, host="0.0.0.0", port=port)