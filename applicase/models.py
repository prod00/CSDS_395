from typing import Tuple
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


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
    case_id = models.CharField(max_length=10)
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
    department = models.CharField(max_length=45, default="other")

    def __str__(self):
        return self.section

class RAPositionPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=100)  # e.g.
    department = models.CharField(max_length=100)
    key_words = models.CharField(max_length=500)  # this will be a list of easily searchable words to filter for students
    description = models.TextField()

    def __str__(self):
        return self.title

class TAApplication(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(default=timezone.now)
    position = models.ForeignKey(TAPositionPost, on_delete=models.CASCADE)

    GRADE_TYPES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("P", "P"),
    ]

    taken = models.BooleanField(default=False)  # the bool for if the student has take the class
    grade = models.CharField(max_length=1, choices=GRADE_TYPES)  # This will be out of 100 to organize the students by grade
    year = models.IntegerField(default=2000)  # 2020.5 if it was fall, 2020 if spring. Allow for another way to organize
    semester = models.CharField(max_length=6, default="spring")
    professor = models.CharField(max_length=50)  # First and Last name of the professor they took course with
    comment = models.TextField()  # Anything else the student may want to add

    def __str__(self):
        return str(self.user)

class Courses(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=112)
    department = models.CharField(max_length=45)
    credits = models.FloatField(max_length=1)

    def __str__(self):
        return self.code

class MajorMinor(models.Model):
    name = models.CharField(max_length=67, primary_key=True)
    is_major = models.BooleanField()
    is_minor = models.BooleanField()

    def __str__(self):
        return self.name

class Departments(models.Model):
    department = models.CharField(max_length=45, primary_key=True)
    
    def _str_(self):
        return self.department

class StudentInterests(models.Model):
    username = models.CharField(max_length=150)
    interest = models.CharField(max_length=45)

    class Meta:
        unique_together = ('username', 'interest',)

    def _str_(self):
        return self.interest

class TAPositionChat(models.Model):
    members = models.ManyToManyField(User, related_name="ta_chat_members")
    position = models.ForeignKey(TAPositionPost, on_delete=models.CASCADE)

    def _str_(self):
        return self.position


class RAPositionChat(models.Model):
    members = models.ManyToManyField(User, related_name="ra_chat_members")
    position = models.ForeignKey(RAPositionPost, on_delete=models.CASCADE)

    def _str_(self):
        return self.position

class RAApplication(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(default=timezone.now)
    position = models.ForeignKey(RAPositionPost, on_delete=models.CASCADE)

    comment = models.TextField()

    def __str__(self):
        return self.user