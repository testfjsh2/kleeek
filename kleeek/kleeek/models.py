# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class roomType(models.Model):
    name = models.CharField(max_length=30)
    typeKleeek = models.CharField(max_length=30)
    image = models.ImageField(upload_to='img')

class roomManager(models.Model):
    roomTypeID = models.ForeignKey(roomType)
    roomPosition = models.IntegerField()
    dateCreate = models.DateField()
    dateLost = models.DateField()
    ownderID = models.IntegerField()
    ownerName = models.CharField(max_length=30)
    ownerLastName = models.CharField(max_length=30)
    lastClickDate = models.DateField()
    status = models.CharField(max_length=20)

class roomLog(models.Model):
    roomManager = models.OneToOneField(roomManager)
    oldOwners = models.TextField()

class payment(models.Model):
    userID = models.OneToOneField(User)
    userGold = models.IntegerField()
    userSilver = models.IntegerField()
    userBronze = models.IntegerField()
    dayBonus = models.IntegerField()