from django.db import models

class Pack(models.Model):
    topic = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    finished = models.IntegerField(default=0)   

class Problem(models.Model):
    probQuestion = models.TextField(max_length=2000)
    probAnswer = models.CharField(max_length=1000)
    story = models.CharField(max_length=5000)
    numOrder = models.IntegerField(default=0)
    packId = models.ForeignKey(Pack, on_delete=models.CASCADE)