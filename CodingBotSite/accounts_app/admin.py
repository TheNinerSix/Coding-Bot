from django.contrib import admin

# Register your models here.
from .models import School, Student, Professor, UserType


class SchoolAdmin(admin.ModelAdmin):
    # fields to display in the django admin database view
    list_display = ('pk', 'schoolName', 'email', 'password')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'firstName', 'lastName', 'email', 'password', 'schoolID')


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'firstName', 'lastName', 'email', 'password', 'schoolID')


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'userType')


admin.site.register(School, SchoolAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(UserType, UserTypeAdmin)
