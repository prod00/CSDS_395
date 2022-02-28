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
from .forms import StudentSignUpForm, ProfessorSignUpForm, StudentInterestsForm, TAPositionPostForm, TAApplicationForm
from .models import User, Student, Professor, TAPositionPost, TAApplication

def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_home')
        else:
            return redirect('professor_home')
    return render(request, 'registration/signup.html')

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
                post_id = key.replace('post_id','')
                applied = True
        if applied:
            new_ta_application_form = TAApplicationForm(request.POST)
            if new_ta_application_form.is_valid():
                user = request.user.student
                position = TAPositionPost.objects.get(id=int(post_id))
                taken = new_ta_application_form.cleaned_data['taken']
                grade = new_ta_application_form.cleaned_data['grade']
                semester = new_ta_application_form.cleaned_data['semester']
                professor = new_ta_application_form.cleaned_data['professor']
                comment = new_ta_application_form.cleaned_data['comment']

                new_application = TAApplication.objects.create(user=user,
                                                                position=position,
                                                                taken=taken,
                                                                grade=grade,
                                                                semester=semester,
                                                                professor=professor,
                                                                comment=comment)
                new_application.save()
                messages.success(request, 'The TA application for '+str(position.section)+' has been sent!')
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
    ta_post_form = TAPositionPostForm()
    professor_posts = TAPositionPost.objects.filter(user=request.user).order_by('-date_posted')
    context = {
        'ta_post_form': ta_post_form,
        'posts': professor_posts,
    }
    return render(request, 'applicase/professor_home.html', context)

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('student_home')

def studentuniqueID(request):
    messages.success(request, 'Case ID must be unique')
    return redirect('student_signup')

class ProfessorSignUpView(CreateView):
    model = User
    form_class = ProfessorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'professor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        login(self.request, form.save())
        return redirect('professor_home')

@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'applicase/interests_form.html'
    success_url = reverse_lazy('student_home')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)

def ta_post_submit(request):
    position_form = TAPositionPostForm(request.POST)
    if request.method == 'POST':
        if position_form.is_valid():
            section = position_form.cleaned_data['section']
            description = position_form.cleaned_data['description']
            print(section, description)
            user = request.user
            new_position = TAPositionPost.objects.create(section=section, description=description, user=user)
            new_position.save()
            messages.success(request, 'The TA position has been posted!')

            return redirect('professor_home')

    else:
        ta_post_form = TAPositionPostForm()
        return render(request, 'applicase/professor_home.html', {'ta_post_form': ta_post_form})

