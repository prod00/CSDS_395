from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from applicase.models import Student, Subject, User,StudentYear

class StudentSignUpForm(UserCreationForm):
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

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        student.year.add(self.cleaned_data.get('year'))
        return user

class ProfessorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_professor = True
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