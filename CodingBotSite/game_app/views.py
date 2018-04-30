from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import View
from .forms import studentGameForm
from .models import Problem, Pack
from course_app.models import Progress, Enrollment, Course
from account_app.models import Student

# Create your views here.
# Views are functions that return html
def index(request):
    context = {}
    return render(request, 'game/studentGame.html', context)

#getters and setters

def setPackId(object):
	global pack_id
	pack_id = object

def getPackId():
	return pack_id
	
def setProblemId(object):
	global problem_id
	problem_id = object

def getProblemId():
	return problem_id
	
def setStudentId(object):
	global student_id
	student_id = object

def getStudentId():
	return student_id
	
def setEnrollmentId(object):
	global enrollment_id
	enrollment_id = object

def getEnrollmentId():
	return enrollment_id
	
def setProgressId(object):
	global progress_id
	progress_id = object

def getProgressId():
	return progress_id
	
class studentGameFormView(View):
	form_class = studentGameForm
	template_name = "game/studentGame.html"
	
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

#handles story and question display

class ProblemFormView(View):
	#get ids for problems in pack
	studentID = getStudentId()
	#student = Enrollment.objects.get(studentId=studentID)
	student = Enrollment.objects.get(studentId=studentID, courseId = courseID)
	setEnrollmentId(student.pk)
	#get studnet progress for problems
	flag = False
	for i in range(1, 5):
		problem = Progress.objects.get(enrollmentID = getEnrollmentId(), packID = getPackId(), numOrder = i)
		setProgressId(problem.pk)
		if problem.completed == 0:
			flag = True
			break
				
	#find first problem not completed by student
	if flag:
		#get problem table
		setProblemId(problem.pk)
		
		#print story
		#print problem
		
		GameplayFormView(View)
	else:
		#print message about pack completed
		return redirect('student')

#handles answering the question

class GameplayFormView(View):
	form_class = GameplayForm
	template_name = "game/studentGame.html"
	studentID = request.student.pk
	
	def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
		
	def post(self, request):
		#The line below should be getting the user input into input variable
		
		input = self.form_class(request.POST)
		prob = Problem.objects.get(pk = getProblemId)
		progress = Progress.objects.get(pk = getProgressId)
		progress.attempt= progress.attempts++
		stud = Student
		temp = input.replace(";", "")
		temp2 = temp.replace("{", "")
		cleanedInput = temp2.replace("}", "")
		mainMethod = re.sub(r'_+', cleanedInput, prob.probQuestion)
		textFile = "Student"+ getStudentId()+ ".txt"
		className= "Student"+ getStudentId()
		file = open(textFile, "w")
		file.write("public class " + className + " {")
		file.write(mainMethod)
		file.write("}")
		file.close
		#docker start answer-checker
		output = subprocess.run("docker exec -it answer-checker bash -c 'cd ./volume; javac " +textFile+ " ; java "+className+"'", shell=True)
		os.remove(textFile)
		#check output against database
		if output==prob.probAnswer
			progress.completed = 1
			progress.save()
			ProblemFormView(View)
		else
			progress.save()
			GameplayFormView(View)