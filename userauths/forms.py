from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

class UserRegisterForm(UserCreationForm):
	full_name = forms.CharField(label='Enter fullname', widget=forms.TextInput(attrs={"class":"form-control"}))
	username = forms.CharField(label='Enter username', widget=forms.TextInput(attrs={"class":"form-control"}))
	phone = forms.CharField(label='Enter phone number', widget=forms.TextInput(attrs={"class":"form-control"}))
	email = forms.EmailField(label='Enter email id', widget=forms.EmailInput(attrs={"class":"form-control"})) 
	password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput(attrs={"class":"form-control"}))
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={"class":"form-control"}))
	
	class Meta:
		model = User
		fields = ['full_name', 'username', 'phone', 'email', 'password1', 'password2']
		
	