from django.contrib import admin

# Register your models here.
from .models import Course, Progress, Enrollment, Connection


class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'sectionNum', 'maxCapacity', 'numEnrolled', 'openDate', 'closeDate', 'classCode', 'professorID')


class ProgressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'problemID', 'packID', 'enrollmentID', 'completed', 'attempts')


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'studID', 'courseID')


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'packID', 'courseID')


admin.site.register(Course, CourseAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Connection, ConnectionAdmin)
