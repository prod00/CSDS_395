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
    section = models.CharField(max_length=50, default="XXXX")
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

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    case_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    case_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year = models.ManyToManyField(StudentYear, related_name='year_students')
    interests = models.ManyToManyField(Subject, related_name='interested_students')

    def __str__(self):
        return self.user.username

class TAPositionPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    section = models.CharField(max_length=9)  # e.g. CSDS 492
    description = models.TextField()

    def __str__(self):
        return self.section


class TAApplication(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(default=timezone.now)
    position = models.ForeignKey(TAPositionPost, on_delete=models.CASCADE)

    taken = models.BooleanField(default=False)  # the bool for if the student has take the class
    grade = models.FloatField(max_length=4)  # This will be out of 100 to organize the students by grade
    semester = models.FloatField(max_length=6)  # 2020.5 if it was fall, 2020 if spring. Allow for another way to organize
    professor = models.CharField(max_length=50)  # First and Last name of the professor they took course with
    comment = models.TextField()  # Anything else the student may want to add

class Courses(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=112)
    department = models.CharField(max_length=45)
    credits = models.FloatField(max_length=1)

class MajorMinor(models.Model):
    name = models.CharField(max_length=67, primary_key=True)
    is_major = models.BooleanField()
    is_minor = models.BooleanField()
