from django.contrib import admin

# Register your models here.
from .models import Pack, Problem


class PackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'topic', 'description', 'finished')


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'numOrder', 'packId')


admin.site.register(Pack, PackAdmin)
admin.site.register(Problem, ProblemAdmin)
