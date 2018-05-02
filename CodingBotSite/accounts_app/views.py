from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import View
from .forms import UserRegistrationForm, LoginForm, studentMenuForm, AddClassForm
from .models import UserType
from django.shortcuts import render
from course_app.models import Enrollment, Course
from .models import Student, School

# Create your views here.


def index(request):
    context = {}
    return render(request, 'accounts/index.html', context)


# @login_required
def professor(request):
    context = {}
    return render(request, 'accounts/professor.html', context)


# @login_required
def school(request):
    context = {}
    return render(request, 'accounts/school.html', context)


# @login_required
def student(request):
    context = {}
    return render(request, 'accounts/studentMenu.html', context)


class studentMenuFormView(View):
    form_class = studentMenuForm
    template_name = "accounts/studentMenu.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


# @login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def login_error(request):
    context = {}
    return render(request, 'accounts/loginError.html', context)


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

            # test if user is a student, professor, or school, and redirect accordingly
            u = User.objects.get(username=request.user.username)
            user_type = u.usertype.userType
            if user_type == 'STUD':

                # if the student table is already populated for the user, do nothing; else: create the student object
                if Student.objects.filter(userID=request.user.pk).exists():
                    print('DEBUG==============================================Student object EXISTS')
                else:
                    print('DEBUG==============================================Student object does NOT EXIST')
                    # create the student object and populate the table
                    # TODO  Notice: schoolID is currently set to the first school only
                    school_object = School.objects.all()
                    student_object = Student(
                        userID=request.user,
                        schoolID=school_object.first(),
                    )
                    student_object.save()

                student_object = Student.objects.get(userID=request.user)
                # redirect student to addClass.html page if they have not enrolled in any courses
                if Enrollment.objects.filter(studID=student_object).exists():
                    print('DEBUG===============================Student is enrolled in a course')
                    return redirect('student')
                else:
                    print('DEBUG===============================Student is NOT enrolled in a course')
                    # redirect them to the 'add class' page
                    return redirect('add_class')

            elif user_type == 'PROF':
                return redirect('professor')
            elif user_type == 'SCHL':
                return redirect('school')
            else:
                return redirect('login_error')
        else:
            # Return an 'invalid login' error message
            return redirect('https://www.google.com/')

        # return render(request, self.template_name, {'form': form})


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
            # Save the form data in an object, but don't save to database. (Note: form.save gathers all other
            #   data like email and username, so it doesnt need to be cleaned and explicitly set for new_student.
            new_student = form.save(commit=False)
            clean_password = form.cleaned_data['password']
            new_student.set_password(clean_password)
            new_student.save()

            # Add the type of user (in this case: student) to the user types table
            new_user_type = UserType.objects.create(
                user=new_student,
                userType='STUD'
            )
            new_user_type.save()

            # redirect them to the login page so they can now login with their account
            return redirect('login')

        # if register fails return register page
        return render(request, self.template_name, {'form': form})


class AddClassFormView(View):
    form_class = AddClassForm
    template_name = 'accounts/addClass.html'

    # handles GET requests/displays blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # handles POST requests/processes form data when user hits submit
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # query Student table for student ID by using the userID
            print('Student.objects.get(userID=request.user.pk) returned: ' + str(request.user.pk))
            student_id = Student.objects.get(userID=request.user.pk)

            # get courseID from course table by using class code the student entered from the form
            class_code = str(form.cleaned_data['class_code'])
            print('str(form.cleaned_data[class_code] returned: ' + class_code)
            course_id = Course.objects.get(classCode=class_code)

            # create new Enrollment table instance
            new_enrollment = Enrollment(
                studID=student_id,
                courseID=course_id,
            )

            # save the new instance of the enrollment table
            new_enrollment.save()

            # TODO Initialize all the progress for the problems




            # redirect them to the login page so they can now login with their account
            return redirect('student')

        # if register fails return register page
        return render(request, self.template_name, {'form': form})
