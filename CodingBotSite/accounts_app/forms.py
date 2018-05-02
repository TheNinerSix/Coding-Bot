from django.contrib.auth.models import User
from django import forms
# from django.forms import ModelForm
# from .models import Student


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


class studentMenuForm(forms.Form):
    input = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id':'commandLine','autofocus':'autofocus','autocomplete':'off'}))


class AddClassForm(forms.Form):
    class_code = forms.CharField(max_length=30)
