from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("upload-resume/", views.upload_resume, name="upload_resume"),
    path("learning-path/", views.learning_path, name="learning_path"),
]
