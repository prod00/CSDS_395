from django.contrib import admin
from .models import Student, Subject, User, StudentYear, TAPositionPost, TAApplication, RAApplication, RAPositionPost, Professor, Courses, MajorMinor

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Subject)
admin.site.register(StudentYear)
admin.site.register(TAPositionPost)
admin.site.register(TAApplication)
admin.site.register(RAApplication)
admin.site.register(RAPositionPost)
admin.site.register(Courses)
admin.site.register(MajorMinor)
