from django import forms
from django.contrib.auth.models import User
from .models import Pass
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

class AddPassForm(forms.ModelForm):
    class Meta():
        model = Pass
        fields = ['PassNumber', 'FullName', 'ContactNumber', 'Email', 'IdentityCardno', 'IdentityType', 'category', 'Source', 'Destination', 'FromDate', 'ToDate', 'Cost']
        widgets = {
            'PassNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'FullName': forms.TextInput(attrs={'class': 'form-control'}),
            'ContactNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'IdentityCardno': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'Source': forms.TextInput(attrs={'class': 'form-control'}),
            'Destination': forms.TextInput(attrs={'class': 'form-control'}),
            'FromDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ToDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'Cost': forms.TextInput(attrs={'class': 'form-control'}),
            'IdentityType': forms.TextInput(attrs={'class': 'form-control'}),
        }