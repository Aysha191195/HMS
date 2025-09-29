from django import forms
from .models import Patient, Doctor, Appointment, Bill

class PatientForm(forms.ModelForm):
    class Meta: model = Patient; fields = '__all__'

class DoctorForm(forms.ModelForm):
    class Meta: model = Doctor; fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta: model = Appointment; fields = '__all__'

class BillForm(forms.ModelForm):
    class Meta: model = Bill; fields = '__all__'
