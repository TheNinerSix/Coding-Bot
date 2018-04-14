from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Views are functions that return html
def index(request):
    context = {}
    return render(request, 'game/studentGame.html', context)