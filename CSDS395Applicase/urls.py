"""CSDS395Applicase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from applicase.views import StudentSignUpView, ProfessorSignUpView, SignUpView, StudentInterestsView, student_home, \
    professor_home, home, studentuniqueID, ta_post_submit, ta_applications

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/professor/', ProfessorSignUpView.as_view(), name='professor_signup'),
    path('accounts/profile/', home, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name="logout"),
    path('', home, name='home'),
    path('home/student/', student_home, name='student_home'),
    path('home/professor/', professor_home, name='professor_home'),
    path('interests/', StudentInterestsView.as_view(), name='student_interests'),
    path('signup/integrity-error', studentuniqueID, name='integrity-error'),
    path('professor/ta-post/', ta_post_submit, name='ta-post'),
    path('professor/<int:pk>/applications', ta_applications, name='ta_applications')

]


