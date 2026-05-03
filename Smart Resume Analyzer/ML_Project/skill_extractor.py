import pandas as pd
import os

def extract_skills(resume_text):
    # Get the directory of the current file and construct path to skills.csv
    current_dir = os.path.dirname(os.path.abspath(__file__))
    skills_csv_path = os.path.join(current_dir, "data", "skills.csv")
    
    skills_db = pd.read_csv(skills_csv_path, header=None)
    found_skills = []

    resume_text = resume_text.lower()

    for skill in skills_db[0]:
        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills
