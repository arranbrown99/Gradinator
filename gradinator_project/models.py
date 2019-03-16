from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class User(models.Model):
	GUID = models.FloatField(max_length=7, unique=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	email = models.EmailField(blank=True, unique=True)
	GPA = models.IntegerField(max_length=3)
class Course(models.Model):
	ID = models.CharField(max_length=30, unique=True)
	taught_by = models.CharField(max_length=30)
	description = models.TextField(default="")
	required_grades = 