from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect, reverse
from applicase.models import Student, Subject, User, StudentYear, Professor, TAPositionPost, TAApplication


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

# class TAPositionPostForm(forms.Form):
#     section = forms.CharField(max_length=9, label="Section (ex. MATH 101):")
#     description = forms.CharField(widget=forms.Textarea)
#     class Meta:
#         model = TAPositionPost
#         fields = ['section', 'description']

class TAApplicationForm(forms.Form):
    GRADE_TYPES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("P", "P"),
    ]
    taken = forms.BooleanField(required=True, label="Verify that you have taken this course before:")
    grade = forms.ChoiceField(choices=GRADE_TYPES, label="Grade in the class")
    year = forms.FloatField(label="Year you took the class (add .5 for fall semester)")
    professor = forms.CharField(max_length=50, label="First and last name of professor")
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TAApplication
        fields = ['taken', 'grade', 'year', 'professor', 'comment']

class RAApplicationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TAApplication
        fields = ['message']
