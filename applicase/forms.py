from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect, reverse
from applicase.models import Student, Subject, User, StudentYear, Professor, TAPositionPost, TAApplication

class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    case_id = forms.CharField(max_length=10)
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    year = forms.ModelChoiceField(
        queryset=StudentYear.objects.all(),
        widget=forms.RadioSelect,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'case_id']


    @transaction.atomic
    def save(self):


        user = super().save(commit=False)
        user.is_student = True
        user.username = self.cleaned_data.get('case_id')
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        student.year.add(self.cleaned_data.get('year'))
        return user





class ProfessorSignUpForm(UserCreationForm):
    case_id = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'case_id']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_professor = True
        user.username = self.cleaned_data.get('case_id')
        professor = Professor.objects.create(user=user)
        #professor.save()
        if commit:
            user.save()
        return user

class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }
class StudentYearForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('year', )
        widgets = {
            'year': forms.CheckboxInput
        }

class TAPositionPostForm(forms.Form):
    section = forms.CharField(max_length=9)
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = TAPositionPost
        fields = ['section', 'description']

class TAApplicationForm(forms.Form):
    GRADE_TYPES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("P", "P"),
    ]
    taken = forms.BooleanField(label="Check if you have taken the class")
    grade = forms.ChoiceField(choices=GRADE_TYPES, label="Grade in the class")
    semester = forms.FloatField(label="Year you took the class")
    professor = forms.CharField(max_length=50, label="First and last name of professor")
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TAApplication
        fields = ['taken', 'grade', 'semester', 'professor', 'comment']
