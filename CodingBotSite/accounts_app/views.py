from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Views are functions that return html
def index(request):
    context = {}
    return render(request, 'accounts/index.html', context)

def professor(request):
    context = {}
    return render(request, 'accounts/professor.html', context)

def register(request):
    context = {}
    return render(request, 'accounts/register.html', context)

def school(request):
    context = {}
    return render(request, 'accounts/school.html', context)

def student(request):
    context = {}
    return render(request, 'accounts/studentMenu.html', context)