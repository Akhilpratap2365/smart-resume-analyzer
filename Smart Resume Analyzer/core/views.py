from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
import os
import sys

# ✅ FIX PATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ML_Project'))

# ✅ IMPORTS
from ML_Project.model import predict_category, predict_top_k
from ML_Project.role_skills import ROLE_SKILLS
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills


# ============================================
# Home Page
# ============================================
def home(request):
    return render(request, "core/home.html")


# ============================================
# About Page
# ============================================
def about(request):
    return render(request, "about.html")


# ============================================
# Contact Page
# ============================================
def contact(request):
    if request.method == "POST":
        return render(request, "contact.html", {"success": True})
    return render(request, "contact.html")


# ============================================
# Login Page
# ============================================
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return render(request, "login.html", {"success": True})
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# ============================================
# Register Page
# ============================================
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("password_confirm")

        if password != confirm:
            return render(request, "registration.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "registration.html", {"error": "Username exists"})

        if User.objects.filter(email=email).exists():
            return render(request, "registration.html", {"error": "Email exists"})

        User.objects.create_user(username=username, email=email, password=password)
        return render(request, "registration.html", {"success": True})

    return render(request, "registration.html")


# ============================================
# Resume Upload & Analysis (🔥 MAIN FIXED)
# ============================================
@require_http_methods(["GET", "POST"])
def upload_resume(request):
    if request.method == "POST":

        if "resume" not in request.FILES:
            return render(request, "upload.html", {"error": "No file selected"})

        file = request.FILES["resume"]

        # ✅ Save file
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            # ✅ Extract text
            resume_text = extract_text_from_pdf(file_path)

            # 🔥 Get top predictions
            top_roles = predict_top_k(resume_text)

            # 🔥 Extract skills
            skills = extract_skills(resume_text)
            skills_lower = [s.lower() for s in skills]

            # 🔥 Choose best role based on skill match
            best_role = None
            best_score = -1

            for role, _ in top_roles:
                required = ROLE_SKILLS.get(role, [])
                match = len(set(skills_lower).intersection(set(required)))

                if match > best_score:
                    best_score = match
                    best_role = role

            # fallback
            role = best_role if best_role else predict_category(resume_text)

            # 🔥 ATS score
            required = ROLE_SKILLS.get(role, [])
            match = len(set(skills_lower).intersection(set(required)))

            if required:
                ats_score = int((match / len(required)) * 100)
            else:
                ats_score = 50

            # 🔥 Missing skills
            missing_skills = [s for s in required if s not in skills_lower]

            context = {
                "skills": skills,
                "role": role,
                "salary": "5-10 LPA",
                "ats_score": ats_score,
                "missing_skills": missing_skills,
            }

            return render(request, "result.html", context)

        except Exception as e:
            return render(request, "upload.html", {"error": str(e)})

    return render(request, "upload.html")


# ============================================
# Learning Path
# ============================================
@require_http_methods(["GET", "POST"])
def learning_path(request):

    if request.method == "POST":
        target_role = request.POST.get("target_role", "")
        skills_str = request.POST.get("skills", "")

        current_skills = [s.strip() for s in skills_str.split(",")] if skills_str else []

        from learning_path import get_learning_path

        try:
            recommendations = get_learning_path(target_role, current_skills)

            return render(request, "learning_path.html", {
                "target_role": target_role,
                "current_skills": current_skills,
                "recommendations": recommendations,
            })

        except Exception as e:
            return render(request, "learning_path.html", {"error": str(e)})

    target_role = request.GET.get("role", "")
    skills_str = request.GET.get("skills", "")
    current_skills = [s.strip() for s in skills_str.split(",")] if skills_str else []

    return render(request, "learning_path.html", {
        "target_role": target_role,
        "current_skills": current_skills,
    })