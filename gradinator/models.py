from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models import *


# Create your models here.


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    guid = models.FloatField(max_length=7, unique=True, primary_key=True)
    GPA = models.IntegerField()
    email = models.EmailField(blank=True, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.7.x, define __unicode__ too!
    def __str__(self):
        return self.user.username


class Course(models.Model):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    taught_by = models.CharField(max_length=30)
    description = models.TextField(default="")
    requirements_of_entry = models.TextField(default="")
    credits = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    school = CharField(max_length=30)
    name = CharField(max_length=30)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    # use this to order courses by each field so school then year then name
    class Meta:
        ordering = ['school', 'year', 'name']


class Coursework(models.Model):
    course = models.ForeignKey(Course, default="")
    weight = models.IntegerField(default=0)
    name = models.CharField(max_length=30, default="")

    class Meta:
        verbose_name_plural = 'Coursework'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Coursework, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserGrade(models.Model):
    # weak entity
    grade_for = models.ForeignKey(Course)
    sat_by = models.ForeignKey(UserProfile)

    grade = IntegerField(3)

    class Meta:
        unique_together = ('grade_for', 'sat_by')


class UserCourseworkGrade(models.Model):
    grade_for = models.ForeignKey(Coursework)
    sat_by = models.ForeignKey(UserProfile)

    grade = FloatField(max_length=3)

    class Meta:
        unique_together = ('grade_for', 'sat_by')
