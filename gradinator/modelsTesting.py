from django.test import TestCase
from gradinator.models import *
import django
from django.core.validators import validate_email


class UserProfileTests(TestCase):

    # def create_test_user(self, username, gpa, email, password):
    #     # print(validate_email(email))
    #
    #     user = User.objects.create_user(username=username, email=email, password=password)
    #     return UserProfile.objects.get_or_create(user=user, GPA=gpa, email=email)[0]
    #
    # def test_ensure_unique_username(self):
    #     user = UserProfileTests.create_test_user(self, 'User1', 21, 'example1@example1.com', 'password')
    #     try:
    #         user2 = UserProfileTests.create_test_user(self, 'User1', 21, 'example1@example1.com', 'password')
    #         self.fail(msg="created non-unique user")
    #     except django.db.utils.IntegrityError:
    #         pass
    #
    # def test_ensure_valid_email(self):
    #     try:
    #         user = UserProfileTests.create_test_user(self, 'User2', 21, 'example1', 'password')
    #     except django.core.validators.ValidationError:
    #         print("pass")

    def create_test_user(self, username, gpa, email, password):
        
        pass

    def test_unique_email(self):
        pass

    def test_valid_email(self):
        pass

    def test_valid_gpa(self):
        # test >=0 and <=22
        # test
        pass


class UserGradeTests(TestCase):
    def test_valid_grade(self):
        pass
