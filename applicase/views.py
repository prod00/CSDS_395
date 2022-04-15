from urllib import request
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .decorators import student_required, professor_required

from .forms import  StudentInterestsForm, TAApplicationForm
from .models import User, Student, Professor, TAPositionPost, TAApplication, Courses, Departments, StudentInterests


def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_home')
        elif request.user.is_professor:
            return redirect('professor_home')
        else:
            return render(request, 'registration/signup.html')
    else:
        return render(request, 'applicase/landing_page.html')

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'



@student_required
def student_home(request):
    professor_posts = TAPositionPost.objects.all().order_by('-date_posted')
    student_applications = TAApplication.objects.filter(user=request.user.student).order_by('-date_applied')
    ta_application_form = TAApplicationForm()
    user_interests = []
    posts = []
    applications = []
    for interest in request.user.student.interests.get_queryset():
        user_interests.append(interest.section)
    for post in professor_posts:
        for ui in user_interests:
            if ui in post.section:
                posts.append(post)

    for app in student_applications:
        for post in posts:
            if post.id == app.position.id:
                applications.append(app)
                posts.remove(post)

    applied = False
    post_id = None

    if request.method == 'POST':
        for key, value in request.POST.items():
            if 'post_id' in key:
                post_id = key.replace('post_id', '')
                applied = True
        if applied:
            new_ta_application_form = TAApplicationForm(request.POST)
            if new_ta_application_form.is_valid():
                user = request.user.student
                position = TAPositionPost.objects.get(id=int(post_id))
                taken = new_ta_application_form.cleaned_data['taken']
                grade = new_ta_application_form.cleaned_data['grade']
                float_year = new_ta_application_form.cleaned_data['year']
                if int(float_year) != float_year:
                    semester = "fall"
                else:
                    semester = "spring"
                year = int(float_year)
                professor = new_ta_application_form.cleaned_data['professor']
                comment = new_ta_application_form.cleaned_data['comment']

                new_application = TAApplication.objects.create(user=user,
                                                               position=position,
                                                               taken=taken,
                                                               grade=grade,
                                                               year=year,
                                                               semester=semester,
                                                               professor=professor,
                                                               comment=comment)
                new_application.save()
                messages.success(request, 'The TA application for ' + str(position.section) + ' has been sent!')
                return redirect('student_home')
    context = {
        'posts': posts,
        'ta_application_form': ta_application_form,
        'applications': applications,

    }
    return render(request, 'applicase/student_home.html', context)
    # return render(request, 'applicase/index.html', context)


@professor_required
def professor_home(request):
    classes = Courses.objects.all()
    #ta_post_form = TAPositionPostForm()
    professor_posts = TAPositionPost.objects.filter(user=request.user).order_by('-date_posted')
    context = {
        #'ta_post_form': ta_post_form,
        'posts': professor_posts,
        'classes': classes,
    }
    return render(request, 'applicase/professor_home.html', context)


# class StudentSignUpView(CreateView):
#     model = User
#     template_name = 'registration/signup_form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'student'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('student_home')


def studentuniqueID(request):
    messages.success(request, 'Case ID must be unique')
    return redirect('student_signup')


def is_student(request):
    user = request.user
    new_user = Student(user=user, first_name=user.first_name, last_name=user.last_name,
                                      case_id=user.username)

    user.is_student = True
    user.is_professor = False
    user.save()
    new_user.save()
    print(user.is_student)
    return redirect('student_home')


def is_professor(request):
    user = request.user
    new_professor = Professor(user=user, first_name=user.first_name, last_name=user.last_name,
                                        case_id=user.username)
    user.is_professor = True
    user.is_student = False
    user.save()
    new_professor.save()
    return redirect('professor_home')


# class ProfessorSignUpView(CreateView):
#     model = User
#     form_class = ProfessorSignUpForm
#     template_name = 'registration/signup_form.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'professor'
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         login(self.request, form.save())
#         return redirect('professor_home')

def StudentInterestsView(request):
    departments = Departments.objects.all().order_by('department')
    currentInterests = StudentInterests.objects.filter(username = request.user.username)
    context = {
        'departments': departments,
        'interests': currentInterests
    }
    return render(request, 'applicase/interests_form.html', context)



def ta_post_submit(request):
    #position_form = TAPositionPostForm(request.POST)
    if request.method == 'POST':
        print(request.POST)
        section = request.POST['classes']
        description = request.POST['description']
        user = request.user
        new_position = TAPositionPost.objects.create(section=section, description=description, user=user)
        new_position.save()
        messages.success(request, 'The TA position has been posted!')

        return redirect('professor_home')



@professor_required
def ta_applications(request, pk=1):

    ta_apps = TAApplication.objects.filter(position__user=request.user, position_id=pk).order_by('-date_applied')
    post = TAPositionPost.objects.get(pk=pk)
    context = {"applications": ta_apps,
               "post": post}
    return render(request, 'applicase/professor_TAapplications.html', context)


# def ta_application_modal(request, pk=1):
#     classes = Courses.objects.all()
#     context = {"classes": classes}
#     return render(request, 'applicase/createTApostmodal.html', context)

def student_interest_update(request):
    interests = request.POST.getlist("interests")
    oldInterests = StudentInterests.objects.filter(username = request.user.username)
    oldInterests.delete()
    for interest in interests:
        new_interest = StudentInterests.objects.create(username = request.user.username, interest = interest)
        new_interest.save()
    return redirect('student_home')