from django.db import models
from userauth.models import User
# Create your models here.


class Categories(models.Model):
	createdbyuser = models.ForeignKey(User, models.CASCADE)
	title = models.CharField(max_length=30)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

class Content(models.Model):
	user = models.ForeignKey(User, models.CASCADE)
	title = models.CharField(max_length=30)
	body = models.CharField(max_length=300)
	summary = models.CharField(max_length=60)
	document = models.FileField(upload_to ='content-documents/')
	Categories=models.ManyToManyField(Categories)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

