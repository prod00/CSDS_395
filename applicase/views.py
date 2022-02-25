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
from .forms import StudentSignUpForm, ProfessorSignUpForm, StudentInterestsForm, TAPositionPostForm
from .models import User, Student, Professor, TAPositionPost

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
    context = {

    }
    return render(request, 'applicase/student_home.html', context)

@professor_required
def professor_home(request):
    ta_post_form = TAPositionPostForm()
    context = {
        'ta_post_form': ta_post_form,
    }
    print("HI",ta_post_form)
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
        user = form.save()
        login(self.request, user)
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
    print('BOOBS')
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
            print("DIDNT WORK")

    else:
        print('BOOBS')
        ta_post_form = TAPositionPostForm()
        return render(request, 'applicase/professor_home.html', {'ta_post_form': ta_post_form})