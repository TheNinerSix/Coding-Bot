from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, default=0)


class Student(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    schoolID = models.ForeignKey(School, on_delete=models.CASCADE)


class Professor(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    schoolID = models.ForeignKey(School, on_delete=models.CASCADE)


''' 
    Class: UserType
    Links with a one-to-one relationship to the Django user model
    Used to differentiate types of users including: student, professor, and school
    View Django documentation: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#extending-the-existing-user-model
'''


class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    STUDENT = 'STUD'
    PROFESSOR = 'PROF'
    SCHOOL = 'SCHL'
    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
        (SCHOOL, 'School'),
    )
    userType = models.CharField(max_length=4, choices=USER_TYPE_CHOICES, default=STUDENT)
