from django.contrib import admin
from .models import Doctor, Patient, Appointment, Bill

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Only include fields that exist in Doctor model
    list_display = ('name', 'specialization')  # make sure these are actual fields
    search_fields = ['name', 'specialization']  # list, not string
    list_filter = ['specialization']  # list, not string

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender')  # adjust according to your Patient model
    search_fields = ['name']
    list_filter = ['gender']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'status')  # adjust to actual fields
    search_fields = ['patient__name', 'doctor__name']
    list_filter = ['status']

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'status')  # adjust to actual fields
    search_fields = ['patient__name']
    list_filter = ['status']
