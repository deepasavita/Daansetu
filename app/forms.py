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

from django import forms
from .models import Donor  # Adjust the import as needed for your project

class DonorSignupForm(forms.ModelForm):
    userpic = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Donor
        fields = ['contact', 'userpic', 'address']
        widgets = {
            'contact': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Full Address'}),
        }
