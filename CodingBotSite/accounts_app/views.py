from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import View
from .forms import UserRegistrationForm, LoginForm, studentMenuForm, classCreationForm, classEditForm
from .models import UserType, Professor, Student, School
from django.shortcuts import render
from course_app.models import Course, Enrollment, Connection
from game_app.models import Pack

# Create your views here.


def index(request):
	context = {}
	return render(request, 'accounts/index.html', context)
	
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	
@login_required
def professor(request):
	thisProfessor = Professor.objects.get(userID = request.user)
	professorName = request.user.username
	courses = Course.objects.all().filter(professorID=thisProfessor).values('name','id')
	return render(request, 'accounts/professor.html', {'courses':courses, 'professorName':professorName})

	
class classEditFormView(View):
	form_class = classEditForm
	
	def get(self, request):
		form = self.form_class(None)
		thisProfessor = Professor.objects.get(userID = request.user)
		courses = Course.objects.all().filter(professorID=thisProfessor).values('name','id')
		thisCourse = Course.objects.get(id = request.GET['courseID'])
		usedPacks = Connection.objects.all().filter(courseID = thisCourse)
		unusedPacks = Pack.objects.all().exclude(pk__in=usedPacks)
		if Enrollment.objects.filter(courseID = request.GET['courseID']):
			studentEnrollment = Enrollment.objects.get(courseID = request.GET['courseID'])
			studentsIDs = Student.objects.all().filter(pk = studentEnrollment.studID.pk)
			roster = User.objects.all().filter(pk__in=studentsIDs.values('userID')).values('first_name','last_name','email')
			return render(request, 'accounts/professorView.html', {'roster':roster, 'courses':courses, 'thisCourse':thisCourse, 'usedPacks':usedPacks, 'unusedPacks':unusedPacks})
		else:
			roster = ""
			return render(request, 'accounts/professorView.html', {'roster':roster, 'courses':courses, 'thisCourse':thisCourse, 'usedPacks':usedPacks, 'unusedPacks':unusedPacks})
	
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			course = Course.objects.get(id = request.GET['courseID'])
			form = self.form_class(request.POST, instance = course)
			form.save()
			return redirect('professor')
		else:
			raise ValueError("Invalid Input")
		
class classCreationFormView(View):
	form_class = classCreationForm

	def get(self, request):
		form = self.form_class(None)
		thisProfessor = Professor.objects.get(userID = request.user)
		courses = Course.objects.all().filter(professorID=thisProfessor).values('name','id')
		return render(request, 'accounts/professorCreate.html', {'form':form, 'courses':courses, 'thisProfessor':thisProfessor})
		
	def post(self, request):
		thisProfessor = Professor.objects.get(userID = request.user)
		form = self.form_class(request.POST)    
		if form.is_valid():
			form.instance.professorID = thisProfessor
			new_course = form.save(commit=False)
			new_course.save()
			new_connection = Connection.objects.create(
				packID = Pack.objects.get(pk = 1),
				courseID = new_course
			)
			new_connection2 = Connection.objects.create(
				packID = Pack.objects.get(pk = 2),
				courseID = new_course
			)
			new_connection3 = Connection.objects.create(
				packID = Pack.objects.get(pk = 3),
				courseID = new_course
			)
			new_connection.save()
			new_connection2.save()
			new_connection3.save()
			return redirect('professor')

		return render(request, 'accounts/professorCreate.html', {'form': form})

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# @login_required
def school(request):
	schoolName = request.user.username
	return render(request, 'accounts/school.html', {'schoolName':schoolName})

# view all the accounts in the school page
def schoolView(request):
	thisSchool = School.objects.get(userID = request.user)
	professors = Professor.objects.all().filter(schoolID=thisSchool)
	students = Student.objects.all().filter(schoolID=thisSchool)
	professorData = User.objects.all().filter(pk__in=professors.values('userID')).values('username','first_name','last_name','email')
	studentData = User.objects.all().filter(pk__in=students.values('userID')).values('username','first_name','last_name','email')
	return render(request, 'accounts/schoolView.html', {'professorData':professorData, 'studentData':studentData})

# handles the creation of a professor in the school page
class professorCreationFormView(View):
	form_class = UserRegistrationForm
	template_name = 'accounts/schoolCreate.html'

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
			thisSchool = School.objects.get(userID = request.user)
			new_professor = form.save(commit=False)
			clean_password = form.cleaned_data['password']
			new_professor.set_password(clean_password)
			new_professor.save()
			
            # Add the type of user (in this case: student) to the user types table
			new_user_type = UserType.objects.create(
				user=new_professor,
				userType='PROF'
			)
			new_user_type.save()
			
			new_schoolProf = Professor.objects.create(
				userID = new_professor,
				schoolID = thisSchool
			)
			
            # redirect them to the login page so they can now login with their account
			return redirect('school')

        # if register fails return register page
		return render(request, self.template_name, {'form': form})

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
				return redirect('student')
			elif user_type == 'PROF':
				return redirect('professor')
			elif user_type == 'SCHL':
				return redirect('school')
			else:
				return redirect('login_error')
		else:
            # Return an 'invalid login' error message
			return redirect('https://www.google.com/')

		return render(request, self.template_name, {'form': form})

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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


