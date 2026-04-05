from django import forms
from .models import Bill, Challan
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['project_name', 'client_name', 'client_address', 'client_phone', 'billing_date', 'price', 'gst_rate']
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ChallanForm(forms.ModelForm):
    class Meta:
        model = Challan
        fields = ['project_name', 'client_name', 'client_address', 'delivery_date', 'description']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }
