from django.db import models

class School(models.Model):
    schoolName = models.CharField(max_length=500) 
    email = models.CharField(max_length=500)    # this field could be changed to an EmailField and also max_length shortened
    password = models.CharField(max_length=700)

class Student(models.Model):
    firstName = models.CharField(max_length=500)
    lastName = models.CharField(max_length=500)
    email = models.CharField(max_length=500)    # this field could be changed to an EmailField and also max_length shortened
    password = models.CharField(max_length=700)
    schoolID = models.ForeignKey(School, on_delete=models.CASCADE)

class Professor(models.Model):
    firstName = models.CharField(max_length=500)
    lastName = models.CharField(max_length=500)
    email = models.CharField(max_length=500)    # this field could be changed to an EmailField and also max_length shortened
    password = models.CharField(max_length=700)
    schoolID = models.ForeignKey(School, on_delete=models.CASCADE)