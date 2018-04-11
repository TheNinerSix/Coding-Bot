from django.contrib import admin

# Register your models here.
from .models import School, Student, Professor

admin.site.register(School)
admin.site.register(Student)
admin.site.register(Professor)
