from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())





class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter your address'}))
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
