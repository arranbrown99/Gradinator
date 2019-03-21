from django.test import TestCase
from django.core.urlresolvers import reverse


class AccountTesting(TestCase):


# do this testing

class My_Course_testing(TestCase):
    def test_view_no_courses(self):
        pass

    def test_view_all_categories(self):
        pass


class show_course_testing(TestCase):
    def test_show_invalid_course(self):
        pass

    def test_show_valid_course(self):
        pass


class enrol_testing(TestCase):
    def test_enrolled_order_by_year(self):
        pass

    def test_enrol_all_enrolled(self):
        pass

    def test_enroll_none_enrolled(self):
        pass


class band_calculator_testing(TestCase):
    def test_valid_prediction(self):
        pass
