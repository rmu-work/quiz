import requests
from django import forms
from django.contrib.auth import authenticate, login

from .models import User


class RegisterForm(forms.ModelForm):
    mobile_number = forms.CharField(widget=forms.NumberInput)

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'email',
            'mobile_number',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(requests, username=username, password=password)

        if not user:
            raise forms.ValidationError('Invalid credentials.!!')

        self.user = user # noqa

        return self.cleaned_data

    def login(self, request):
        if hasattr(self, 'user'):
            login(request, self.user)

