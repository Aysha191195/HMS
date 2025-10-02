from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import Patient, Doctor, Appointment, Bill
from .forms import PatientForm, DoctorForm, AppointmentForm, BillForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
import json
from django.utils.timezone import now
from datetime import timedelta
from .models import Patient

def home(request):
    context = {
        'patients_count': Patient.objects.count(),
        'doctors_count': Doctor.objects.count(),
        'appointments_count': Appointment.objects.count(),
        'bills_count': Bill.objects.count(),
        'appointments': Appointment.objects.all().order_by('-date')[:5],
    }
    return render(request, 'home.html', context)

def patients(request):
    risk_filter = request.GET.get('risk')
    patients = Patient.objects.all()

    if risk_filter:
        patients = patients.filter(risk_level=risk_filter)

    return render(request, "patients.html", {"patients": patients})
def add_patient(request):
    form = PatientForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(); return redirect('patients')
    return render(request, 'add_patient.html', {'form': form})

def edit_patient(request, id):
    obj = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); return redirect('patients')
    return render(request, 'edit_patient.html', {'form': form})

def delete_patient(request, id):
    obj = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        obj.delete(); return redirect('patients')
    return render(request, 'delete_patient.html', {'patient': obj})

# Doctors
def doctors(request):
    objs = Doctor.objects.all(); return render(request, 'doctors.html', {'doctors': objs})
def add_doctor(request):
    form = DoctorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('doctors')
    return render(request, 'add_doctor.html', {'form': form})
def edit_doctor(request, id):
    obj = get_object_or_404(Doctor, id=id); form = DoctorForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('doctors')
    return render(request, 'edit_doctor.html', {'form': form})
def delete_doctor(request, id):
    obj = get_object_or_404(Doctor, id=id)
    if request.method == 'POST': obj.delete(); return redirect('doctors')
    return render(request, 'delete_doctor.html', {'doctor': obj})

# Appointments
def appointments(request):
    objs = Appointment.objects.select_related('patient', 'doctor').all(); return render(request, 'appointments.html', {'appointments': objs})
def add_appointment(request):
    form = AppointmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('appointments')
    return render(request, 'add_appointment.html', {'form': form})
def edit_appointment(request, id):
    obj = get_object_or_404(Appointment, id=id); form = AppointmentForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('appointments')
    return render(request, 'edit_appointment.html', {'form': form})
def delete_appointment(request, id):
    obj = get_object_or_404(Appointment, id=id)
    if request.method == 'POST': obj.delete(); return redirect('appointments')
    return render(request, 'delete_appointment.html', {'appointment': obj})

# Bills
def bills(request):
    objs = Bill.objects.select_related('patient').all(); return render(request, 'bills.html', {'bills': objs})
def add_bill(request):
    form = BillForm(request.POST or None)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('bills')
    return render(request, 'add_bill.html', {'form': form})
def edit_bill(request, id):
    obj = get_object_or_404(Bill, id=id); form = BillForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('bills')
    return render(request, 'edit_bill.html', {'form': form})
def delete_bill(request, id):
    obj = get_object_or_404(Bill, id=id)
    if request.method == 'POST': obj.delete(); return redirect('bills')
    return render(request, 'delete_bill.html', {'bill': obj})

# Reports & PDF
def reports(request):
    appointments = Appointment.objects.select_related('patient','doctor').all()
    bills = {b.patient.id: b for b in Bill.objects.all()}
    report_data = []
    for appt in appointments:
        report_data.append({'patient': appt.patient,'doctor': appt.doctor,'date': appt.date,'time': appt.time,'prescription': appt.prescription or 'No prescription','bill': bills.get(appt.patient.id)})
    return render(request, 'reports.html', {'report_data': report_data})

def download_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=report.pdf'
    p = canvas.Canvas(response, pagesize=A4)
    y = 800
    appointments = Appointment.objects.select_related('patient','doctor').all()
    bills = {b.patient.id: b for b in Bill.objects.all()}
    for appt in appointments:
        bill = bills.get(appt.patient.id)
        p.setFont('Helvetica', 11)
        p.drawString(50, y, f"{appt.patient.name} - {appt.doctor.name} ({appt.date})")
        y -= 20
        p.drawString(70, y, f"Prescription: {appt.prescription or 'N/A'}")
        y -= 20
        if bill:
            p.drawString(70, y, f"Bill: ₹{bill.amount} - {bill.status}")
        else:
            p.drawString(70, y, 'Bill: Not Generated')
        y -= 40
        if y < 100:
            p.showPage(); y = 800
    p.save(); return response

def generate_invoice(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    bill = Bill.objects.filter(patient=patient).first()
    appointments = Appointment.objects.filter(patient=patient).select_related('doctor')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{patient.name}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    y = 800
    p.setFont('Helvetica-Bold', 16); p.drawString(200, y, 'Hospital Invoice'); y -= 50
    p.setFont('Helvetica', 12); p.drawString(50, y, f"Patient: {patient.name}, Age: {patient.age}, Gender: {patient.gender}"); y -= 30
    for appt in appointments:
        p.drawString(50, y, f"Appointment: {appt.date} with {appt.doctor.name}"); y -= 20
        p.drawString(70, y, f"Prescription: {appt.prescription or 'N/A'}"); y -= 30
        if y < 100: p.showPage(); y = 800
    if bill: p.drawString(50, y, f"Bill Amount: ₹{bill.amount}, Status: {bill.status}")
    else: p.drawString(50, y, 'Bill Not Generated')
    p.save(); return response

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Registration successful. Login now.")
            return redirect('login')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')