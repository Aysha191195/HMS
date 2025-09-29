from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    availability = models.CharField(max_length=100, default='9AM - 5PM')
    contact = models.CharField(max_length=15, blank=True)
    def __str__(self): return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact = models.CharField(max_length=15, null=True, blank=True)  # ✅ auto timestamp
    registered_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, default='Scheduled')
    prescription = models.TextField(blank=True, null=True)
    def __str__(self): return f"{self.patient.name} with {self.doctor.name}"

class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Paid','Paid'),('Unpaid','Unpaid')], default='Unpaid')
    def __str__(self): return f"Bill for {self.patient.name} - {self.amount}"
