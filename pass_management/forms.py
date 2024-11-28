from django import forms
from django.contrib.auth.models import User
from .models import *
from .models import Pass, Category, Location
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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'emailid', 'contact', 'message', 'msgdate', 'isread']


class RouteCostForm(forms.ModelForm):
    class Meta:
        model = RouteCost
        fields = ['source', 'destination', 'base_cost']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
class PassForm(forms.ModelForm):
    class Meta:
        model = Pass
        fields = [
            'PassNumber', 'FullName', 'ContactNumber', 'Email', 'IdentityType', 
            'IdentityCardno', 'category', 'Source', 'Destination', 
            'FromDate', 'ToDate', 'Cost'
        ]
        widgets = {
            'PassNumber': forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Auto-generated pass number'}),  # Make pass number readonly
            'FullName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'ContactNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'IdentityType': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the type of identity card'}),
            'IdentityCardno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your identity card number'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'Source': forms.Select(attrs={'class': 'form-control'}),  # Using Select for ForeignKey
            'Destination': forms.Select(attrs={'class': 'form-control'}),  # Using Select for ForeignKey
            'FromDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ToDate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Cost': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),  # Keep cost read-only
        }

    # Override the __init__ method to make sure ForeignKey fields load data correctly
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically set the queryset for 'Source', 'Destination', and 'category' if needed
        self.fields['Source'].queryset = Location.objects.all()  # All Location objects for Source
        self.fields['Destination'].queryset = Location.objects.all()  # All Location objects for Destination
        self.fields['category'].queryset = Category.objects.all()  # All Category objects for category

        # Automatically calculate cost once the form is initialized, if needed
        if self.instance.pk:  # If the object exists (e.g., editing), set cost
            self.instance.set_cost()  # If `set_cost` exists on the model

    def clean(self):
        cleaned_data = super().clean()
        
        # Optionally add custom validation here
        from_date = cleaned_data.get('FromDate')
        to_date = cleaned_data.get('ToDate')
        
        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError('The start date cannot be later than the end date.')

        return cleaned_data