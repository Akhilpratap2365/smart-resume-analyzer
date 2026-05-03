import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_skill_gap_chart(current_skills, missing_skills):
    skills = current_skills + missing_skills
    status = [1] * len(current_skills) + [0] * len(missing_skills)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))

    sns.barplot(x=skills, y=status, palette="viridis")

    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Skill Status (1 = Known, 0 = To Learn)")
    plt.xlabel("Skills")
    plt.title("Skill Gap Analysis")

    # Create path relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    charts_dir = os.path.join(base_dir, "static", "charts")
    os.makedirs(charts_dir, exist_ok=True)
    
    chart_path = os.path.join(charts_dir, "skill_gap.png")

    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path
