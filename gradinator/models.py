from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import *
from django.db.models import *

# Create your models here.

# use this to order courses by each field so school then year probably
# class Meta:
#    ordering = ['', '', '']


class User(models.Model):
    GUID = models.FloatField(max_length=7, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    email = models.EmailField(blank=True, unique=True)
    GPA = models.IntegerField(max_length=3)


class Course(models.Model):
    ID = models.CharField(max_length=30, unique=True)
    taught_by = models.CharField(max_length=30)
    description = models.TextField(default="")
    required_grades = models.CharField(default="")
    credits = models.IntegerField(max_length=3)
    year = IntegerField(max_length=3)
    school = CharField(max_length=30)
    name = CharField(max_length=30)


class CourseWork(models.Model):
    course = Course.ID
    weight = IntegerField(max_length=3)
    name = Course.name


class UserGrade:
    grade_for = Course.ID
    grade = IntegerField(3)
    SatBy = User.GUID


class UserCourseGrade:
    grade_for = CourseWork.name
    user = User.GUID
    grade = FloatField(max_length=3)



