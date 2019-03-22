from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, primary_key=True)
    # The additional attributes we wish to include.
    GPA = models.IntegerField(default=0)
    email = models.EmailField(default="", blank=True, )
    picture = models.ImageField(upload_to='profile_images', default='media/blank.png')

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.7.x, define __unicode__ too!
    def __str__(self):
        return self.user.username


class Course(models.Model):
    id = models.CharField(max_length=30, primary_key=True, unique=True)
    taught_by = models.CharField(max_length=30)
    description = models.CharField(max_length=1000, default="")
    requirements_of_entry = models.TextField(default="")
    credits = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    year = models.IntegerField(default=1, validators=[MaxValueValidator(4), MinValueValidator(1)])
    school = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    url = models.URLField(max_length=250, default="")

    slug = models.SlugField()

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
    weight = models.FloatField(default=0, validators=[MaxValueValidator(100), MinValueValidator(1)])
    name = models.CharField(max_length=30, default="", unique=True)

    slug = models.SlugField(default="")

    class Meta:
        verbose_name_plural = 'Coursework'
        ordering = ['course']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Coursework, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserGrade(models.Model):
    # weak entity
    grade_for = models.ForeignKey(Course)
    sat_by = models.ForeignKey(UserProfile)

    grade = models.FloatField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])

    class Meta:
        unique_together = ('grade_for', 'sat_by')


class UserCourseworkGrade(models.Model):
    # weak entity
    grade_for = models.ForeignKey(Coursework)
    sat_by = models.ForeignKey(UserProfile)

    grade = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(0)])

    class Meta:
        unique_together = ('grade_for', 'sat_by')
