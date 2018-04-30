from django import forms
from models import *
class StudentForm(forms.ModelForm):
    class Meta:
        model = student
        widgets = {
        'password': forms.PasswordInput(),
    }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = faculty
        widgets = {
        'password': forms.PasswordInput(),
    }


class dean_staff_officeForm(forms.ModelForm):
    class Meta:
        model = dean_staff_office
        widgets = {
        'password': forms.PasswordInput(),
    }