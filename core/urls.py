from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patients, name='patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/edit/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),
    path('bills/', views.bills, name='bills'),
    path('bills/add/', views.add_bill, name='add_bill'),
    path('bills/edit/<int:id>/', views.edit_bill, name='edit_bill'),
    path('bills/delete/<int:id>/', views.delete_bill, name='delete_bill'),
    path('reports/', views.reports, name='reports'),
    path('reports/download/', views.download_report, name='download_report'),
    path('invoice/<int:patient_id>/', views.generate_invoice, name='generate_invoice'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
   
]
