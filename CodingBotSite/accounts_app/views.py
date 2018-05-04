from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import View
from .forms import UserRegistrationForm, LoginForm, CommandLineForm, AddClassForm
from .models import UserType
from django.shortcuts import render
from course_app.models import Enrollment, Course, Progress
from game_app.models import Pack, Problem
from .models import Student, School
import re
import subprocess
import os

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
            messages.add_message(request, messages.ERROR, 'ERROR: A user with those credentials does not exist.')
            # the user does not exist, return the login page
            return redirect('login')


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
            messages.add_message(request,messages.SUCCESS, 'Registration was successful!')
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
            # Error Handling: if the class code they entered exists, perform the query
            # else return them to the add class page
            if Course.objects.filter(classCode=class_code).exists():
                course_id = Course.objects.get(classCode=class_code)
            else:
                return render(request, self.template_name, {'form': form})

            # create new Enrollment table instance
            new_enrollment = Enrollment(
                studID=student_id,
                courseID=course_id,
            )

            # save the new instance of the enrollment table
            new_enrollment.save()

            # ----------------------------------------------------------------------------------------------------------
            # This section of code initializes all the progress records for all the problems in the packs
            # get all the packs
            packs_object = Pack.objects.all()
            # loop through each pack
            for pack in packs_object.iterator():
                # get the problems in the pack
                problems_in_pack_object = Problem.objects.filter(packId=pack)
                # loop through each problem
                for problem in problems_in_pack_object.iterator():
                    # create a new progress record for the student on a particular problem
                    progress_instance = Progress(
                        problemID=problem,
                        packID=pack,
                        enrollmentID=new_enrollment,
                    )
                    # save the new table record
                    progress_instance.save()
            # ----------------------------------------------------------------------------------------------------------

            # redirect them to the student menu page
            return redirect('student')

        # if the form is not valid display a new blank form
        return render(request, self.template_name, {'form': form})


class studentMenuFormView(View):
    form_class = CommandLineForm
    template_name = "accounts/studentMenu.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # ----------------------------------------------------------------------
            # Test if the user entered 'Pack Select', 'Help', or 'Log Out'

            # get the form data
            command = str(form.cleaned_data['input'])

            if command == 'Pack Select':
                return redirect('pack_select')
            elif command == 'Log Out':
                return redirect('logout')
            else:
                return redirect('student')


class PackSelectFormView(View):
    form_class = CommandLineForm
    template_name = "accounts/packSelect.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # ----------------------------------------------------------------------
            # Test if the user entered 'Print Statements', 'If Statements', 'Main Menu', or 'Log Out'

            # get the form data
            command = str(form.cleaned_data['input'])

            if command == 'Print Statements':
                return redirect('game_print_statements')
            elif command == 'If Statements':
                return redirect('game_if_statements')
            elif command == 'Math Functions':
                return redirect('game_math_functions')
            elif command == 'Main Menu':
                return redirect('student')
            elif command == 'Log Out':
                return redirect('logout')
            else:
                return redirect('pack_select')


class GamePrintStatementsFormView(View):
    form_class = CommandLineForm
    template_name = "accounts/gamePrintStatements.html"

    def get(self, request):
        form = self.form_class(None)

        # Get story and problem and send them to the template
        # get the print statement pack
        pack_object = Pack.objects.get(topic='Print Statements')
        pack_id = pack_object
        # get the problems that are in the print statements pack
        problems_queryset = Problem.objects.filter(packId=pack_id)

        # get the first not-completed problem

        user = request.user

        student_object = Student.objects.get(userID=user)
        # get the enrollment table of the student
        enrollment = Enrollment.objects.get(studID=student_object)

        # if there exists a problem in the print statements pack that the
        # student has not completed (completed=0) then get the problem
        # else: TODO: redirect the user to a page to inform them they've already completed the pack
        if Progress.objects.filter(enrollmentID=enrollment).filter(packID=pack_id).filter(completed=0).exists():
            # store the problem id
            current_progress_problem = Progress.objects.filter(enrollmentID=enrollment).filter(packID=pack_id).filter(completed=0).first()
            # set the current progress object (need to set it so we can change the value to completed
            # if the student answers the problem correctly
            set_current_progress_object(current_progress_problem)
            problem_id = current_progress_problem.problemID
            current_problem = Problem.objects.get(pk=problem_id.pk)

            story = current_problem.story
            current_problem_question = current_problem.probQuestion
            # set the question for the problem for later use
            set_problem_question(current_problem_question)
            # get the answer to the problem
            answer = current_problem.probAnswer
            # set the answer for use later in the post request
            set_answer(answer)
            # set the student id for use in the naming of the file in check_answer()
            set_student_id(request.user.id)

            return render(request, self.template_name, {'form': form, 'story': story, 'problem_question': current_problem_question})
        # else: TODO: redirect the user to a page to inform them they've already completed the pack

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # ----------------------------------------------------------------------
            # Test if the user entered 'MainMenu', 'Log Out', or an answer

            # get the form data
            command = str(form.cleaned_data['input'])

            if command == 'Main Menu':
                return redirect('student')
            elif command == 'Log Out':
                return redirect('logout')
            else:
                current_student_answer = get_student_answer()
                # TODO: see if the answer is correct
                bool_correct = check_answer(current_student_answer)
                if bool_correct:
                    # set the problem to completed
                    current_progress = get_current_progress_object()
                    current_progress.completed=1
                    current_progress.save()
                    return redirect('game_print_statements')
                else:
                    # return the same problem
                    return redirect('game_print_statements')


class GameIfStatementsFormView(View):
    form_class = CommandLineForm
    template_name = "accounts/gameIfStatements.html"

    def get(self, request):
        form = self.form_class(None)

        # Get story and problem and send them to the template
        # get the print statement pack
        pack_object = Pack.objects.get(topic='If Statements')
        pack_id = pack_object
        # get the problems that are in the print statements pack
        problems_queryset = Problem.objects.filter(packId=pack_id)

        # get the first not-completed problem

        user = request.user

        student_object = Student.objects.get(userID=user)
        # get the enrollment table of the student
        enrollment = Enrollment.objects.get(studID=student_object)

        # if there exists a problem in the print statements pack that the
        # student has not completed (completed=0) then get the problem
        # else: TODO: redirect the user to a page to inform them they've already completed the pack
        if Progress.objects.filter(enrollmentID=enrollment).filter(packID=pack_id).filter(completed=0).exists():
            # store the problem id
            current_progress_problem = Progress.objects.filter(enrollmentID=enrollment).filter(packID=pack_id).filter(
                completed=0).first()
            # set the current progress object (need to set it so we can change the value to completed
            # if the student answers the problem correctly
            set_current_progress_object(current_progress_problem)
            problem_id = current_progress_problem.problemID
            current_problem = Problem.objects.get(pk=problem_id.pk)

            story = current_problem.story
            current_problem_question = current_problem.probQuestion
            # set the question for the problem for later use
            set_problem_question(current_problem_question)
            # get the answer to the problem
            answer = current_problem.probAnswer
            # set the answer for use later in the post request
            set_answer(answer)
            # set the student id for use in the naming of the file in check_answer()
            set_student_id(request.user.id)

            return render(request, self.template_name,
                          {'form': form, 'story': story, 'problem_question': current_problem_question})
        # else: TODO: redirect the user to a page to inform them they've already completed the pack

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            # get the form data
            command = str(form.cleaned_data['input'])

            if command == 'Main Menu':
                return redirect('student')
            elif command == 'Log Out':
                return redirect('logout')
            else:
                current_student_answer = get_student_answer()
                # TODO: see if the answer is correct
                bool_correct = check_answer(current_student_answer)
                if bool_correct:
                    # set the problem to completed
                    current_progress = get_current_progress_object()
                    current_progress.completed = 1
                    current_progress.save()
                    return redirect('game_if_statements')
                else:
                    # return the same problem
                    return redirect('game_if_statements')


class GameMathFunctionsFormView(View):
    form_class = CommandLineForm
    template_name = "accounts/gameMathFunctions.html"

    def get(self, request):
        form = self.form_class(None)

        # Get story and problem and send them to the template
        # get the print statement pack
        pack_object = Pack.objects.get(topic='Math Functions')
        pack_id = pack_object
        # get the problems that are in the print statements pack
        problems_queryset = Problem.objects.filter(packId=pack_id)

        # get the first not-completed problem

        user = request.user

        student_object = Student.objects.get(userID=user)
        # get the enrollment table of the student
        enrollment = Enrollment.objects.get(studID=student_object)

        # if there exists a problem in the print statements pack that the
        # student has not completed (completed=0) then get the problem
        # else: TODO: redirect the user to a page to inform them they've already completed the pack
        if Progress.objects.filter(enrollmentID=enrollment).filter(packID=pack_id).filter(completed=0).exists():
            # store the problem id
            current_progress_problem = Progress.objects.filter(enrollmentID=enrollment).filter(packID=pack_id).filter(
                completed=0).first()
            # set the current progress object (need to set it so we can change the value to completed
            # if the student answers the problem correctly
            set_current_progress_object(current_progress_problem)
            problem_id = current_progress_problem.problemID
            current_problem = Problem.objects.get(pk=problem_id.pk)

            story = current_problem.story
            current_problem_question = current_problem.probQuestion
            # set the question for the problem for later use
            set_problem_question(current_problem_question)
            # get the answer to the problem
            answer = current_problem.probAnswer
            # set the answer for use later in the post request
            set_answer(answer)
            # set the student id for use in the naming of the file in check_answer()
            set_student_id(request.user.id)

            return render(request, self.template_name,
                          {'form': form, 'story': story, 'problem_question': current_problem_question})
        # else: TODO: redirect the user to a page to inform them they've already completed the pack

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            # get the form data
            command = str(form.cleaned_data['input'])

            if command == 'Main Menu':
                return redirect('student')
            elif command == 'Log Out':
                return redirect('logout')
            else:
                current_student_answer = get_student_answer()
                # TODO: see if the answer is correct
                bool_correct = check_answer(current_student_answer)
                if bool_correct:
                    # set the problem to completed
                    current_progress = get_current_progress_object()
                    current_progress.completed = 1
                    current_progress.save()
                    return redirect('game_math_functions')
                else:
                    # return the same problem
                    return redirect('game_math_functions')


def check_answer(my_student_answer):
    # get the answer to the problem
    correct_answer = get_answer()
    # get the student input
    student_answer_pre_parse = my_student_answer

    temp = student_answer_pre_parse.replace(";", "")
    temp2 = temp.replace("{", "")
    cleanedInput = temp2.replace("}", "")
    # puts answer into question
    my_problem_question = get_problem_question()
    mainMethod = re.sub(r'_+', cleanedInput, my_problem_question)

    # creates and writes to file
    textFile = "runFileDocker/volume/student" + str(get_student_id()) + ".txt"
    className = "student" + str(get_student_id())
    file = open(textFile, "w")
    file.write("public class " + className + " {\n")
    file.write(mainMethod)
    file.write("\n}")
    file.close()
    subprocess.run("cp "+textFile+" runFileDocker/volume/"+className+".java", shell=True)
    # ------------------------------------------------------
    # for testing purposes, delete after testing done
    #output=True
    # ------------------------------------------------------
    # gets output from docker and removes file
    subProcess = subprocess.run(
         "sudo docker exec -it answer-checker bash -c 'cd ./volume; javac " + className + ".java ; java " + className + "'",
         stdout=subprocess.PIPE, shell=True)
    os.remove(textFile)
    os.remove("runFileDocker/volume/"+className+".java")
    output = str(subProcess.stdout)[2:][:-1]

    print("----------------------------------------------------"+str(output))

    # check output against database
    if str(output) == correct_answer:
        return True
    else:
        return False


def set_student_id(my_student_id):
    global current_student_id
    current_student_id=my_student_id


def get_student_id():
    return current_student_id


def set_problem_question(question):
    global problem_question
    problem_question=question


def get_problem_question():
    return problem_question


def set_student_answer(answer):
    global student_answer
    student_answer=answer


def get_student_answer():
    return student_answer


def set_answer(answer):
    global problem_answer
    problem_answer=answer


def get_answer():
    return problem_answer


def set_current_progress_object(progress_object):
    global current_progress_object
    current_progress_object=progress_object


def get_current_progress_object():
    return current_progress_object
