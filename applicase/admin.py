from django.contrib import admin
from .models import Student, Subject, User, StudentYear

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(StudentYear)
admin.site.register(User)