from django import forms
from .models import Education, Hobbies
from Home.models import Person


class EducationForm(forms.ModelForm):
    Institute = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    From = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))
    Till = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Education
        fields = ("Degree", "Institute", "From", "Till")

        widgets = {
            'Degree': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'required': 'False'}),
        }


class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobbies
        fields = ("Hobby",)

        widgets = {
            'Hobby': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }


class IntroForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ("Age", "Address", "Phone", "Profession", "Status", "ProfilePicture")

        widgets = {
            'Address' : forms.TextInput(attrs={'class': 'form-control','type': 'text'}),
            'Profession' : forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'Status' : forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'Age': forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}),
            'Phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
        }