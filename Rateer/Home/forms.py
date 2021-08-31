from django import forms
from django.contrib.auth.models import User
from .models import Person, Feedback


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")

        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'email' : forms.TextInput(attrs={'class': 'form-control','type': 'email'}),
            'password' : forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("Age", "Status", "Address", "Phone", "ProfilePicture", "Profession")

        widgets = {
            'Age': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'Status': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'Address': forms.TextInput(attrs={'class': 'form-control','type': 'text'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'Profession': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'ProfilePicture': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("UserName", "Subject", "Message")

        widgets = {
            'UserName' : forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'Subject' : forms.TextInput(attrs={'class': 'form-control','type': 'text'}),
            'Message': forms.Textarea(attrs={'class': 'form-control', 'type': 'text'}),
        }