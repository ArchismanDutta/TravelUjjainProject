from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer

class CustomerSignupForm(UserCreationForm):
    username = forms.CharField(
        min_length=8,  # ✅ Minimum 8 characters
        max_length=150,
        required=True,
        help_text='Required. 8 characters or more. Letters, digits and @/./+/-/_ only.'
    )
    password1 = forms.CharField(
    label="Password",
    widget=forms.PasswordInput,
    help_text="Minimum 8 characters, must include a letter and a number."
)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password1', 'password2']

class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
