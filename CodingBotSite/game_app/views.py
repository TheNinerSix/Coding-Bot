from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic import View
from .forms import studentGameForm
from .models import Problem, Pack
from course_app.models import Progress, Enrollment, Course
from accounts_app.models import Student
from subprocess import run
from os import remove


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
	
def setCourseId(object):
	global course_id
	course_id = object

def getCourseId():
	return course_id
	

#question answering
def ProblemFormView(View):
	#get ids for problems in pack
	studentID = getStudentId()
	courseID = getCourseId()
	#gets enrollmentID for student in specific class
	student = Enrollment.objects.get(studentId=studentID, courseId = courseID)
	setEnrollmentId(student.pk)
	
	flag = False
	#will run until pack is completed
	while True:
		#searches for first not completed question
		for i in range(1, 5):
			problemProgress = Progress.objects.get(enrollmentID = getEnrollmentId(), packID = getPackId(), numOrder = i)
			setProgressId(problemProgress.pk)
			if problem.completed == 0:
				flag = True
				break
				
		#find first problem not completed by student
		if flag:
			setProblemId(problemProgress.problemID)
		
			#WRITE: print story
			#WRITE: print problem
		
		else:
			#WRITE: print message about pack completed
			break

		while True:
			#The line below should be getting the user input into input variable
			input = self.form_class(request.POST)
			#gets problem
			problem = Problem.objects.get(pk = getProblemId())
			#increases attempts
			problemProgress.attempt= problemProgress.attempts + 1
			#cleans input
			temp = input.replace(";", "")
			temp2 = temp.replace("{", "")
			cleanedInput = temp2.replace("}", "")
			#puts answer into question
			mainMethod = re.sub(r'_+', cleanedInput, problem.probQuestion)
			
			#creates and writes to file
			textFile = "Student"+ getStudentId()+ ".txt"
			className= "Student"+ getStudentId()
			file = open(textFile, "w")
			file.write("public class " + className + " {")
			file.write(mainMethod)
			file.write("}")
			file.close
			
			#gets output from docker and removes file
			output = subprocess.run("docker exec -it answer-checker bash -c 'cd ./volume; javac " +textFile+ " ; java "+className+"'", shell=True)
			os.remove(textFile)
			
			#check output against database
			if output == problem.probAnswer:
				#if correct marks as completed and fields saves to the database and moves to next question
				problemProgress.completed = 1
				problemProgress.save()
				break
			else:
				#if not correct save field to database and run in database
				problemProgress.save()
	#WRITE: line that moves back to student menu