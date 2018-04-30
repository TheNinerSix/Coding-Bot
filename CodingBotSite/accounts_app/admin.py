from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

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


class UserTypeInline(admin.StackedInline):
    model = UserType
    can_delete = False
    verbose_name_plural = 'User Types'


class UserAdmin(BaseUserAdmin):
    inlines = (UserTypeInline, )
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')


admin.site.register(School, SchoolAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
