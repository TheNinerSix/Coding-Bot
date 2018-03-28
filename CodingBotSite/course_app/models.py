from django.db import models

Class Course(models.Model):
    name = models.CharField(max_length=200)
    sectionNum = models.CharField(max_length=20)
    maxCapacity = models.IntegerField(default=0)
    numEnrolled = models.IntegerField(default=0)
    openDate = models.DateTimeField('Open Date')
    closeDate = models.DateTimeField('Close Date')
    professorID = models.ForeignKey(Professor, on_delete=CASCADE())

Class Progress(models.Model):
    problemID = models.ForeignKey(Problem, on_delete=CASCADE())
    completed = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)

Class Enrollment(models.Model):
    studID = models.ForeignKey(Student, on_delete=CASCADE())
    courseID = models.ForeignKey(Course, on_delete=CASCADE())
    progressID = models.ForeignKey(Progress, on_delete=CASCADE())

Class Connection(models.Model):
    packID = models.ForeignKey(Pack, on_delete=CASCADE())
    courseID = models.ForeignKey(Course, on_delete=CASCADE())