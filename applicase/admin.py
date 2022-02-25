from django.contrib import admin
from .models import Student, Subject, User, StudentYear, TAPositionPost, Professor

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Subject)
admin.site.register(StudentYear)
admin.site.register(TAPositionPost)
