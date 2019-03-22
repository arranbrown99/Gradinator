from django import forms

from gradinator.models import UserCourseworkGrade
from gradinator.models import UserGrade
from gradinator.models import UserProfile


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user', 'GPA')


class UserGradeForm(forms.ModelForm):
    class Meta:
        model = UserGrade
        exclude = {'grade', 'sat_by', 'grade_for'}


class UserCourseworkGradeForm(forms.ModelForm):
    grade = forms.IntegerField(help_text="Please enter what percentage you got in", required=True)

    class Meta:
        model = UserCourseworkGrade
        exclude = {'sat_by', 'grade_for'}
