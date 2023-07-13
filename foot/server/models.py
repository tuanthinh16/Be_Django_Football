from django.db import models

# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=300)
    username = models.CharField(max_length=200, default='default')
    password = models.CharField(max_length=200, default='default', null=False)
    userID = models.CharField(max_length=200, null=True),
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    timecreated = models.DateTimeField(auto_now_add=True)
