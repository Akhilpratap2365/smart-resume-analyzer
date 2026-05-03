from flask import Flask, render_template, request
import os

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from model import predict_job_role, predict_salary
from ats_score import calculate_ats_score
from learning_path import get_learning_path
from charts import generate_skill_gap_chart

app = Flask(__name__)

# -------------------------------
# Skill formatter for UI display
# -------------------------------
def format_skill(skill):
    skill_map = {
        "sql": "SQL",
        "java": "JAVA",
        "aws": "AWS",
        "html": "HTML",
        "css": "CSS",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "power bi": "Power BI",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "data analysis": "Data Analysis",
        "python": "Python",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "excel": "Excel",
        "flask": "Flask",
        "django": "Django"
    }

    return skill_map.get(skill.lower(), skill.title())


# Register formatter as Jinja filter
app.jinja_env.filters["format_skill"] = format_skill


# -------------------------------
# File upload configuration
# -------------------------------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Resume Upload & Analysis
# -------------------------------
@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files["resume"]

    if file.filename == "":
        return "No file selected"

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Process resume
    resume_text = extract_text_from_pdf(file_path)
    skills = extract_skills(resume_text)
    role = predict_job_role(skills)
    salary = predict_salary(skills)
    ats_score = calculate_ats_score(skills, resume_text)

    # Normalize skills for logic checks
    normalized_skills = [s.lower() for s in skills]

    # Read optional user choices from the upload form
    user_target_role = request.form.get("target_role")
    if user_target_role:
        chosen_role = user_target_role
    else:
        chosen_role = role

    user_willing = [s.lower() for s in request.form.getlist("willing_skills")]

    return render_template(
        "result.html",
        skills=skills,
        role=chosen_role,
        salary=salary,
        ats_score=ats_score,
        known_skills=normalized_skills,
        pre_willing_skills=user_willing
    )


# -------------------------------
# Learning Path Route
# -------------------------------
@app.route("/learning-path", methods=["POST"])
def learning_path_route():
    target_role = request.form["target_role"]

    # Current skills from resume
    skills_str = request.form["skills"]
    current_skills = [s.strip().lower() for s in skills_str.split(",")]

    # Skills user is willing to learn
    willing_skills = [s.lower() for s in request.form.getlist("willing_skills")]

    # Get missing skills for role
    all_missing = get_learning_path(target_role, current_skills)

    # Final recommendations (exclude already chosen skills)
    final_suggestions = [
        skill for skill in all_missing if skill not in willing_skills
    ]

    # 🔥 GENERATE SKILL GAP CHART (THIS WAS MISSING)
    chart_path = generate_skill_gap_chart(
        current_skills,
        final_suggestions
    )

    return render_template(
        "learning_path.html",
        target_role=target_role,
        current_skills=current_skills,
        willing_skills=willing_skills,
        missing_skills=final_suggestions,
        chart_path=chart_path
    )


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
