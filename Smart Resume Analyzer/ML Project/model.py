def predict_job_role(skills):
    skills = [s.lower() for s in skills]

    roles = {
        "Frontend Developer": [
            "html", "css", "javascript", "react", "angular"
        ],
        "Backend Developer": [
            "java", "spring boot", "python", "flask", "django", "node.js"
        ],
        "Full Stack Developer": [
            "html", "css", "javascript", "react",
            "python", "flask", "django", "java", "spring boot"
        ],
        "Data Analyst": [
            "excel", "sql", "power bi", "tableau",
            "data analysis", "statistics",
            "pandas", "numpy",
            "matplotlib", "seaborn"
        ],

        "Data Scientist": [
            "python", "machine learning", "statistics",
            "pandas", "numpy", "scikit-learn",
            "matplotlib", "seaborn"
        ],

        "ML Engineer": [
            "machine learning", "deep learning",
            "tensorflow", "scikit-learn"
        ],
        "DevOps Engineer": [
            "aws", "docker", "kubernetes", "linux", "git"
        ]
    }

    role_scores = {}

    for role, role_skills in roles.items():
        score = 0
        for rs in role_skills:
            if rs in skills:
                score += 1
        role_scores[role] = score

    best_role = max(role_scores, key=role_scores.get)

    if role_scores[best_role] == 0:
        return "Software Engineer"

    return best_role


def predict_salary(skills):
    base_salary = 300000   # 3 LPA
    bonus = len(skills) * 60000
    return base_salary + bonus
