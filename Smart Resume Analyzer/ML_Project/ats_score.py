from ML_Project.role_skills import ROLE_SKILLS


def calculate_ats_score(skills, role):
    # Normalize skills
    skills_lower = [s.lower() for s in skills]

    # Get required skills for role
    required = ROLE_SKILLS.get(role, [])

    # If role not found
    if not required:
        return 50

    # Convert to sets (avoid duplicates)
    skills_set = set(skills_lower)
    required_set = set(required)

    # 🔥 Match calculation
    matched_skills = skills_set.intersection(required_set)

    match_count = len(matched_skills)
    total_required = len(required_set)

    # 🔥 Base score
    score = (match_count / total_required) * 100

    # 🔥 Bonus for strong match (advanced touch)
    if match_count >= total_required * 0.7:
        score += 10

    # 🔥 Penalty if too few skills
    if match_count <= 1:
        score -= 10

    # Clamp between 0–100
    score = max(0, min(int(score), 100))

    return score