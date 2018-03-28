from django.db import models

Class Pack(models.Model):
    topic = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    fininshed = models.IntegerField(default=0)   

Class Problem(models.Model):
    probQuestion = models.CharField(max_length=2000)
    probAnswer = models.CharField(max_length=1000)
    story = models.CharField(max_length=5000)
    packId = models.ForeignKey(Pack, on_delete=models.CASCADE())