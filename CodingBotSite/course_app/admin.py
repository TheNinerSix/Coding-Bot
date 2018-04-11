from django.contrib import admin

# Register your models here.
from .models import Course, Progress, Enrollment, Connection

admin.site.register(Course)
admin.site.register(Progress)
admin.site.register(Enrollment)
admin.site.register(Connection)