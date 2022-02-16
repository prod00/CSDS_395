from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from .decorators import student_required, professor_required
from .forms import StudentSignUpForm, ProfessorSignUpForm, StudentInterestsForm
from .models import User, Student

def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return render(request, 'applicase/student_home.html')
        else:
            return render(request, 'applicase/professor_home.html')
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
    context = {

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

# @method_decorator([login_required, student_required], name='dispatch')
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
