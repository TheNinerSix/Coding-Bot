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



#question answering
def printStoryQuestion(request):
	#gets enrollmentID for student in specific class
	student = Enrollment.objects.get(studentId=request.GET['studentID'], courseId = request.GET['courseID'])
	
	flag = False
	#will run until pack is completed
	#searches for first not completed question
	for i in range(1, 5):
		progress = Progress.objects.get(enrollmentID = student.pk, packID = request.GET['packID'], numOrder = i)
		if problem.completed == 0:
			flag = True
			break
			
	#find first problem not completed by student
	if flag:
		problem = Problem.objects.get(pk = progress.probID)
		return render(request, studentGame.html, {'progress':progress, 'problem':problem})
	
	else:
		#WRITE: print message about pack completed
		return render(request, studentGame.html, "Pack is completed.")

def printStoryQuestion(request):
		#The line below should be getting the user input into input variable
	input = self.form_class(request.POST)
	#gets problem
	problem = Problem.objects.get(pk = request.GET['problem.pk'])
	#increases attempts
	progress = request.GET['progress']
	progress.attempt= progress.attempts + 1
	#cleans input
	temp = input.replace(";", "")
	temp2 = temp.replace("{", "")
	cleanedInput = temp2.replace("}", "")
	#puts answer into question
	mainMethod = re.sub(r'_+', cleanedInput, problem.probQuestion)
	
	#creates and writes to file
	textFile = "runFileDocker/volume/Student"+ getStudentId()+ ".txt"
	className= "Student"+ getStudentId()
	file = open(textFile, "w")
	file.write("public class " + className + " {")
	file.write(mainMethod)
	file.write("}")
	file.close
	
	#gets output from docker and removes file
	output = subprocess.run("docker exec -it answer-checker bash -c 'cd ./volume; javac " +textFile+ " ; java "+className+"'", shell=True)
	os.remove(textFile)
	
	flag = False
	#check output against database
	if output == problem.probAnswer:
		#if correct marks as completed and fields saves to the database and moves to next question
		progress.completed = 1
		progress.save()
		#WRITE: print message about correct
		return render(request, studentGame.html, "Question was answered correct.")
	else:
		#if not correct save field to database and run in database
		progress.save()
		flag = True
		#WRITE: print message about incorrect
		return render(request, studentGame.html, "Question was answered incorrect.")