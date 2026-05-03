def get_learning_path(target_role, current_skills):
    current_skills = [s.lower() for s in current_skills]

    role_skills = {
        "Data Analyst": [
            "excel", "sql", "power bi", "tableau",
            "pandas", "matplotlib", "seaborn", "statistics"
        ],
        "Data Scientist": [
            "python", "machine learning", "statistics",
            "pandas", "numpy", "scikit-learn",
            "matplotlib", "seaborn"
        ],
        "ML Engineer": [
            "machine learning", "deep learning",
            "tensorflow", "scikit-learn", "python"
        ],
        "Frontend Developer": [
            "html", "css", "javascript", "react"
        ],
        "Backend Developer": [
            "python", "flask", "django",
            "java", "spring boot", "sql"
        ],
        "Full Stack Developer": [
            "html", "css", "javascript", "react",
            "python", "flask", "sql"
        ],
        "DevOps Engineer": [
            "aws", "docker", "kubernetes", "linux", "git"
        ]
    }

    required = role_skills.get(target_role, [])
    missing = [skill for skill in required if skill not in current_skills]

    return missing
