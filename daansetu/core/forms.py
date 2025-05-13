from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, ItemDonation, MoneyDonation, VolunteerAssignment

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration
    """
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )
    phone = forms.CharField(
        max_length=15, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control mb-3'})


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom form for user authentication
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))


class ItemDonationForm(forms.ModelForm):
    """
    Form for item donations
    """
    class Meta:
        model = ItemDonation
        fields = ['item_name', 'description', 'quantity', 'condition', 'pickup_address']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 4}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control mb-3', 'min': '1'}),
            'condition': forms.Select(attrs={'class': 'form-select mb-3'}),
            'pickup_address': forms.Textarea(attrs={'class': 'form-control mb-3', 'rows': 3, 'placeholder': 'Enter the address where the item can be picked up'}),
        }


class MoneyDonationForm(forms.ModelForm):
    """
    Form for money donations
    """
    class Meta:
        model = MoneyDonation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'min': '1',
                'step': '0.01'
            }),
        }


class VolunteerAssignmentForm(forms.ModelForm):
    """
    Form for assigning volunteers to item donations
    """
    class Meta:
        model = VolunteerAssignment
        fields = ['volunteer', 'item']
        widgets = {
            'volunteer': forms.Select(attrs={'class': 'form-select mb-3'}),
            'item': forms.Select(attrs={'class': 'form-select mb-3'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show volunteers
        self.fields['volunteer'].queryset = User.objects.filter(role=User.VOLUNTEER)
        # Only show pending items
        self.fields['item'].queryset = ItemDonation.objects.filter(status=ItemDonation.PENDING)
