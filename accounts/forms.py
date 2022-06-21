from django import forms
from accounts.models import *
from django.forms.models import ModelForm
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
import re as regex

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name','first_name', 'last_name', 'phone', 'email', 'address_1', 'address_2', 'city', 'post_code', 'country']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Company Name'
                }),
            'first_name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'First Name',
                'required': True,
                'autofocus':True
                }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Last Name',
                'required': True
                }),
            'phone': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Phone',
                'required': True
                }),
            'email': forms.EmailInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Email Address',
                'required': True
                }),
            'address_1': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Address 1',
                'required': True
                }),
            'address_2': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Address 2'
                }),
            'city': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'City'
                }),
            'post_code': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Post code'
                }),
            'country': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Country'
                })
        }


class StaffNewForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-user', 
            'type':'password', 
            'placeholder':'Password',
            'tabindex':'6'
            }),
        error_messages={
            'required':'Password is required'
        }
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            'class':'form-control form-control-user', 
            'type':'password', 'placeholder':'Confirm Password',
            'tabindex':'7'
            }),
        error_messages={
            'required':'Please confirm password'
        }
    )
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'groups', 'email','password1', 'password2' ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Username',
                'required': True,
                'tabindex':'5'
                }),
            'first_name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'First Name',
                'required': True,
                'tabindex':'1'
                }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Last Name',
                'required': True,
                'tabindex':'2'
                }),
            'groups': forms.CheckboxSelectMultiple(attrs={
                'class':'form-check-input',
                'required': True,
                'tabindex':'4'
                }),
            'email': forms.EmailInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Email Address',
                'required': True,
                'tabindex':'3'
                }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name == "":
            raise forms.ValidationError('First name is required')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name == "":
            raise forms.ValidationError("Last name is required")
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError("Email address is required")
        return email

    def clean_groups(self):
        groups = self.cleaned_data.get("groups")
        print(groups.all())
        if not groups:
            raise forms.ValidationError("Staff must be asigned to a group")
        return groups

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username == "":
            raise forms.ValidationError("Username is required")
        return username

    def clean_password2(self):
        password = self.cleaned_data.get("password2")
        password_regex = "(?=^.{8,15}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&amp;*()_+}{&quot;:;'?/&gt;.&lt;,])(?!.*\s).*$"
        if not regex.search(password_regex, password):
            raise forms.ValidationError("Passwords require a minimum 8 characters and a maximum of 15 characters. It must also contain one uppercase, one lowercase, one number and one special character to be valid.")
        return password



class StaffForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']
        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Username',
                'required': True
                }),
            'first_name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'First Name',
                'required': True
                }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Last Name',
                'required': True
                }),
            'email': forms.EmailInput(attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Email Address',
                'required': True
                }),
            'groups': forms.CheckboxSelectMultiple(attrs={
                'class':'form-check-input',
                'required': True,
                }),
        }
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name == "":
            raise forms.ValidationError('First name is required')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name == "":
            raise forms.ValidationError("Last name is required")
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email == "":
            raise forms.ValidationError("Email address is required")
        return email

    def clean_groups(self):
        groups = self.cleaned_data.get("groups")
        print(groups.all())
        if not groups:
            raise forms.ValidationError("Staff must be asigned to a group")
        return groups

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username == "":
            raise forms.ValidationError("Username is required")
        return username