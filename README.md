# AI Resume Analyzer

A Flask-based web application that analyzes resumes using AI-powered grammar checking, skill detection, and scoring.

## Features

✅ **Resume Upload** - Support for PDF and TXT files
✅ **Skill Detection** - Identifies technical and professional skills
✅ **Grammar Check** - Detects grammar and writing issues
✅ **Resume Scoring** - AI-powered scoring out of 100
✅ **Job Role Matching** - Analyzes resume against target job role
✅ **Recommendations** - Provides actionable improvement suggestions

## Installation

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Spacy Language Model (Optional but Recommended)
```bash
python -m spacy download en_core_web_sm
```

## Running the Application

### Start the Flask Server
```bash
python app.py
```

The app will be available at: **http://localhost:5000**

## Usage

1. **Upload Resume** - Drag & drop or click to upload PDF or TXT file
2. **Enter Job Role** (Optional) - Specify target job position (e.g., "Software Engineer", "Data Analyst")
3. **Paste Job Description** (Optional) - Add job description for better skill matching
4. **Click "Analyze Resume"** - Get results including:
   - Resume Score (0-100)
   - Detected Skills
   - Missing Skills for the role
   - Grammar Issues
   - Recommendations for improvement

## Project Structure

```
resume/
├── app.py              # Flask backend application
├── grammar.py          # Grammar checking module
├── skills.py           # Skill extraction module
├── scoring.py          # Resume scoring module
├── index.html          # Frontend interface
├── script.js           # Frontend JavaScript (deprecated)
└── requirements.txt    # Python dependencies
```

## Technologies Used

- **Backend**: Flask (Python Web Framework)
- **File Processing**: PyPDF2 (PDF extraction)
- **Grammar Check**: LanguageTool
- **NLP**: Spacy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## Troubleshooting

### Port 5000 Already in Use
- Change the port in `app.py`: `app.run(debug=True, host="0.0.0.0", port=8080)`

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Grammar Tool Not Working
The grammar checker is optional. The app will work without it but won't provide grammar suggestions.

### Resume Not Uploading
- Ensure file is PDF or TXT format
- Check file size (should be <10MB)
- Enable console in browser (F12) to see error messages

## API Endpoints

### `GET /`
Returns the HTML interface

### `POST /analyze`
Analyzes uploaded resume

**Request:**
```
Content-Type: multipart/form-data

resume: [file]
job_role: [string] (optional)
job_description: [string] (optional)
```

**Response:**
```json
{
  "score": 75,
  "skills": ["python", "javascript", "react"],
  "missing_skills": ["docker", "kubernetes"],
  "grammar": [{"message": "..."}],
  "recommendations": ["..."],
  "summary": "AI-powered resume analysis completed."
}
```

## License

This project is open source and available for educational use.
