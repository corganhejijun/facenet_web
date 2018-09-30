from django.db import models

class User(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

class Image(models.Model):
    path = models.CharField(max_length=1024)
    belongTo = models.CharField(max_length=128)

class CompareResult(models.Model):
    img1 = models.CharField(max_length=128)
    img2 = models.CharField(max_length=128)
    distance = models.FloatField()