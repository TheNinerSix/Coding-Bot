from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import View
from .forms import studentGameForm


# Create your views here.
# Views are functions that return html
def index(request):
    context = {}
    return render(request, 'game/studentGame.html', context)


class studentGameFormView(View):
    form_class = studentGameForm
    template_name = "game/studentGame.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

