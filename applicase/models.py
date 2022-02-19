from typing import Tuple
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

YEAR_TYPES: Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str], Tuple[str, str], Tuple[str, str]] = (("Freshman", "Freshman"), ("Sophomore", "Sophomore"), ("Junior", "Junior"), ("Senior", "Senior"), ("Other", "Other"))
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

class Subject(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)

class StudentYear(models.Model):
    year = models.CharField(max_length=50)

    def __str__(self):
        return self.year



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    year = models.ManyToManyField(StudentYear, related_name='year_students')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def __str__(self):
        return self.user.username

# class PositionPost(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     title = models.CharField(max_length=100)
#     date_posted = models.DateTimeField(default=timezone.now)