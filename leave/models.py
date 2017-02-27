from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Leave(models.Model):
    username = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()
    daysOfLeave = models.IntegerField(default=0)
    status = models.TextField(choices=(('New',"New Leave"),('Approved',"Approved Leave"),('Declined',"Declined Leave")))

class Employee(models.Model):
    username = models.TextField()
    startDate = models.DateField()
    remainingLeaveDays = models.IntegerField(default=0)