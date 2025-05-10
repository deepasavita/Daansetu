from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm (UserCreationForm):
    password1 = forms.CharField(label='Password', widget-forms.Password Input (attrs={'class': 'form-control',' placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget-forms.Password Input (attrs={'class': 'form-control', 'placeholder': 'Enter Password Again'}))
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets={
        'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter First Name'}),
        'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Last Name'}),
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        'email':forms. EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email ID'}),