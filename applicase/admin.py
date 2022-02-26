from django.contrib import admin
from .models import Student, Subject, User, StudentYear, TAPositionPost, Professor, Courses, MajorMinor

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Subject)
admin.site.register(StudentYear)
admin.site.register(TAPositionPost)
admin.site.register(Courses)
admin.site.register(MajorMinor)
