from django.contrib.auth.forms import UserCreationForm
from django import forms
# from authentication.models import UserProfile
from django.contrib.auth.models import User
from authentication.models import UserProfile

class RegisterPenggunaForm(forms.Form):
    nama = forms.CharField(max_length=255, required=True, label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    gender = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], required=True, label="Gender")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Birthdate")
    address = forms.CharField(widget=forms.Textarea, required=True, label="Address")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Add validation for unique phone number (check in the database)
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone


class RegisterPekerjaForm(forms.Form):
    nama = forms.CharField(max_length=255, required=True, label="Full Name")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    gender = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')], required=True, label="Gender")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Birthdate")
    address = forms.CharField(widget=forms.Textarea, required=True, label="Address")
    bank_name = forms.ChoiceField(choices=[('GoPay', 'GoPay'), ('OVO', 'OVO'), ('Virtual Account BCA', 'Virtual Account BCA'),
                                           ('Virtual Account BNI', 'Virtual Account BNI'), ('Virtual Account Mandiri', 'Virtual Account Mandiri')],
                                  required=True, label="Bank Name")
    account_number = forms.CharField(max_length=20, required=True, label="Account Number")
    npwp = forms.CharField(max_length=15, required=True, label="NPWP")


    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Add validation for unique phone number (check in the database)
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean_npwp(self):
        npwp = self.cleaned_data.get('npwp')
        # Check if the NPWP is unique for all users (both Pekerja and Pengguna)
        if UserProfile.objects.filter(npwp=npwp).exists():
            raise forms.ValidationError("This NPWP is already registered.")
        return npwp

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        bank_name = self.cleaned_data.get('bank_name')
        # Ensure unique combination of bank and account number
        if UserProfile.objects.filter(bank_name=bank_name, account_number=account_number).exists():
            raise forms.ValidationError("This bank account number is already registered for another worker.")
        return account_number


class RoleSelectionForm(forms.Form):
    role = forms.ChoiceField(choices=[('pengguna', 'Pengguna'), ('pekerja', 'Pekerja')], required=True, label="Select Role")
