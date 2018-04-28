from django.db import models
from accounts_app.models import Student, Professor
from game_app.models import Pack, Problem

class Course(models.Model):
    name = models.CharField(max_length=200)
    sectionNum = models.CharField(max_length=20)
    maxCapacity = models.IntegerField(default=0)
    numEnrolled = models.IntegerField(default=0)
    openDate = models.DateTimeField('Open Date')
    closeDate = models.DateTimeField('Close Date')
    professorID = models.ForeignKey(Professor, on_delete=models.CASCADE)

class Enrollment(models.Model):
    studID = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)

class Progress(models.Model):
    problemID = models.ForeignKey(Problem, on_delete=models.CASCADE)
    packID = models.ForeignKey(Pack, on_delete=models.CASCADE, default = 0)
    enrollmentID = models.ForeignKey(Enrollment, on_delete=models.CASCADE, default = 0)
    completed = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)


class Connection(models.Model):
    packID = models.ForeignKey(Pack, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)