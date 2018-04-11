from django.contrib import admin

# Register your models here.
from .models import Pack, Problem

admin.site.register(Pack)
admin.site.register(Problem)