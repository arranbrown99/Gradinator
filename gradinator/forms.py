from django import forms

from gradinator.models import UserProfile
from gradinator.models import UserGrade


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
