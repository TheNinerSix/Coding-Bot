from django.db import models

Class School(models.Model):
    schoolName = models.CharField(max_length=500) 
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=700)

Class Student(models.Model):
    firstName = models.CharField(max_length=500)
    lastName = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=700)
    schoolID = models.ForeignKey(School, on_delete=models.CASCADE())

Class Professor(models.Model):
    firstName = models.CharField(max_length=500)
    lastName = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    password = models.CharField(max_length=700)
    schoolID = models.ForeignKey(School, on_delete=models.CASCADE())