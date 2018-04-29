from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import View
from .forms import UserRegistrationForm, LoginForm
from .models import Student, School
from course_app.models import Course

# Create your views here.
def index(request):
    context = {}
    return render(request, 'accounts/index.html', context)


def professor(request):
    context = {}
    return render(request, 'accounts/professor.html', context)


def school(request):
    context = {}
    return render(request, 'accounts/school.html', context)


def student(request):
    context = {}
    return render(request, 'accounts/studentMenu.html', context)


class LoginFormView(View):
    form_class = LoginForm
    template_name = "accounts/index.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('student')

        else:
            # Return an 'invalid login' error message
            return redirect('https://www.google.com/')

        return render(request, self.template_name, {'form': form})


# handles the registration page logic
class UserRegistrationFormView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    # handles GET requests/displays blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # handles POST requests/processes form data when user hits submit
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # save the form data in an object, but don't save to database
            student = form.save(commit=False)

            # clean and normalize the data
            clean_username = form.cleaned_data['username']
            clean_email = form.cleaned_data['email']
            clean_password = form.cleaned_data['password']
            clean_firstName = form.cleaned_data['first_name']
            clean_lastName = form.cleaned_data['last_name']

            student.set_password(clean_password)
            # save the data to the database
            student.save()

            # returns student object if credentials are correct
            student = authenticate(username=clean_username, password=clean_password)

            # if there is a user that matches the credentials
            if student is not None:
                
                if student.is_active:
                    # log the user in
                    login(request, student)
                    # access user with request.student.first_name
                    return redirect('student')

        # if register fails return register page
        return render(request, self.template_name, {'form': form})