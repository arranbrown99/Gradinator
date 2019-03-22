from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from populate_script import *
from .models import UserProfile


class ModelTests(TestCase):

    # tests for UserProfile
    def create_test_user(self, username, gpa, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return UserProfile.objects.get_or_create(user=user, GPA=gpa, email=email)[0]

    def test_user_unique(self):
        ModelTests.create_test_user(self, 'User1', 21, 'example1@example1.com', 'password')
        try:
            ModelTests.create_test_user(self, 'User1', 21, 'example1@example1.com', 'password')
            self.fail(msg="created non-unique user")
        except IntegrityError:
            pass

    def test_tostring_working(self):
        user1 = ModelTests.create_test_user(self, 'User1', 21, 'example1@example1.com', 'password')

        self.assertEqual(user1.__str__(), user1.user.username)

    def test_valid_gpa(self):
        user1 = ModelTests.create_test_user(self, 'User1', 21, 'example1@example1.com', 'password')

        self.assertTrue(0 <= user1.GPA <= 22)

    # tests for course and coursework
    def test_course_add(self):
        cw = [
            {"name": "jp2 lab exam",
             "course": "jp2",
             "weight": 0.2},
            {"name": "jp2 exam",
             "course": "jp2",
             "weight": 0.6},
            {"name": "jp2 lab 1",
             "course": "jp2",
             "weight": 0.04},
            {"name": "jp2 lab 2",
             "course": "jp2",
             "weight": 0.04},
            {"name": "jp2 lab 3",
             "course": "jp2",
             "weight": 0.04},
            {"name": "jp2 lab 4",
             "course": "jp2",
             "weight": 0.04},
            {"name": "jp2 lab 5",
             "course": "jp2",
             "weight": 0.04},
        ]
        c = {"WAD": {"name": "Web App Development",
                     "id": "COMPSCI 2021",
                     "url": "https://www.gla.ac.uk/coursecatalogue/course/?code=COMPSCI2021",
                     "taught_by": "David Manlove",
                     "description": "The aim of this course is to provide students with a comprehensive overview of web application development. It will provide students with the skills to design and develop distributed web applications in a disciplined manner, using a range of tools and technologies. It will also strengthen their understanding of the context and rationale of distributed systems. ",
                     "requirements_of_entry": "Entry to Level 2 Computing Science is guaranteed to students who achieve a GPA of B3 or better in their level 1 courses at the first sitting. All others would be at the discretion of the School. All grades for Computing Science courses must be at D3 or better at either attempt. Strong python skills are a requirement for this course.",
                     "credits": 10,
                     "year": 2,
                     "school": "School of Computing Science",
                     "coursework": cw}}

        course = add_course_and_coursework(c, cw, "WAD")

        self.assertEqual(course.year, 2)
        self.assertEqual(course.credits, 10)
class ViewsTests(TestCase):
