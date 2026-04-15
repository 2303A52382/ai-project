#Generate a Flask backend application that accepts user skills as input and recommends 
#suitable career roles based on skill matching and also Implement skill gap analysis 
# logic in Python to identify missing skills required for each recommended career role 
# and Add functionality to generate a learning roadmap for each career role based on required skills

from flask import Flask, render_template, request, jsonify
import json
from PyPDF2 import PdfReader

app = Flask(__name__)

with open('data/roles.json') as f:
    roles = json.load(f)

# 🔥 Extract skills from text
def extract_skills(text):
    all_skills = [
        "python", "java", "html", "css", "javascript",
        "machine learning", "data visualization",
        "dsa", "node", "database", "figma"
    ]

    text = text.lower()
    return [skill for skill in all_skills if skill in text]

# 🔥 Read PDF file
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_skills = []

    # ✅ Check file upload
    if 'file' in request.files and request.files['file'].filename != "":
        file = request.files['file']

        if file.filename.endswith('.pdf'):
            text = read_pdf(file)
            user_skills = extract_skills(text)

        elif file.filename.endswith('.txt'):
            text = file.read().decode('utf-8')
            user_skills = extract_skills(text)

    else:
        # fallback to manual input
        skills = request.form.get('skills', '')
        user_skills = [s.strip().lower() for s in skills.split(",")]

    results = []

    for role in roles:
        role_skills = role['skills']

        matched = [s for s in role_skills if s in user_skills]
        missing = [s for s in role_skills if s not in user_skills]

        score = int((len(matched) / len(role_skills)) * 100)

        results.append({
            "role": role['role'],
            "score": score,
            "matched": matched,
            "missing": missing,
            "roadmap": role['roadmap']
        })

    results = sorted(results, key=lambda x: x['score'], reverse=True)

    return jsonify(results[:3])

if __name__ == '__main__':
    app.run(debug=True)