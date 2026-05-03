from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from model import predict_job_role, predict_salary

# make sure this file exists in root folder
resume_path = "sample_resume.pdf"

resume_text = extract_text_from_pdf(resume_path)
skills = extract_skills(resume_text)

job_role = predict_job_role(skills)
salary = predict_salary(skills)

print("Extracted Skills:", skills)
print("Predicted Job Role:", job_role)
print("Predicted Salary: ₹", salary)
