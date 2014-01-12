from django.db import models
from django.contrib.auth.models import User

class roomType(models.Model):
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=50)


class roomManager(models.Model):
    roomTypeID = models.ForeignKey(roomType)
    dateCreate = models.DateField()
    dateLost = models.DateField()
    ownderID = models.IntegerField()
    ownerName = models.CharField(max_length=30)
    lastClickDate = models.DateField()
    status = models.CharField(max_length=20)

class roomLog(models.Model):
    roomManager = models.OneToOneField(roomManager)
    oldOwners = models.TextField()