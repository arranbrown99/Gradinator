from django import forms

from django.contrib.auth.models import User
from gradinator.models import UserProfile


class UserProfileForm(forms.ModelForm):

    email = forms.EmailField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user', 'GPA')
