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
from applicase.views import SignUpView, StudentInterestsView, student_home, \
    professor_home, home, studentuniqueID, ta_post_submit, ta_applications, is_student, is_professor, student_interest_update, add_user_to_ta_chat, user_chats

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/googlesignin/', include("social_django.urls"),name = "social"),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', is_student, name='student_signup'),
    path('accounts/signup/professor/', is_professor, name='professor_signup'),
    path('accounts/profile/', home, name='login_redirect'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name="logout"),
    path('', home, name='home'),
    path('index/', home, name="index"),
    path('home/student/', student_home, name='student_home'),
    path('home/professor/', professor_home, name='professor_home'),
    path('interests/', StudentInterestsView, name='student_interests'),
    path('signup/integrity-error', studentuniqueID, name='integrity-error'),
    path('professor/ta-post/', ta_post_submit, name='ta-post'),
    path('professor/<int:pk>/applications', ta_applications, name='ta_applications'),
    path('student/interest-update/', student_interest_update, name='student-update-interest'),
    path('add/chat_member/<int:pk>', add_user_to_ta_chat, name='add_chat_member'),
    path('chats/', user_chats, name='chats'),
]


