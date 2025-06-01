
from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView
from hospital.forms import CustomAuthForm


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path(
        'adminlogin',
        LoginView.as_view(template_name='hospital/adminlogin.html',authentication_form=CustomAuthForm),name='adminlogin'
    ),
    path(
        'doctorlogin',
        LoginView.as_view(template_name='hospital/doctorlogin.html',authentication_form=CustomAuthForm),name='doctorlogin'
    ),
    path(
        'patientlogin',
        LoginView.as_view(template_name='hospital/patientlogin.html',authentication_form=CustomAuthForm),name='patientlogin'
    ),
    
    
    
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),

    path('adminsignup/', views.admin_signup_view,   name='adminsignup'),
    path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup/', views.patient_signup_view,name='patientsignup'),
    path('activate/<uidb64>/<token>/', views.activate_account_view, name='activate-account'),



    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),
   

    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),
    path('activate/<uidb64>/<token>/', views.activate_account_view, name='activate-account'),
    

    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
    #---------FOR ROOM RELATED URLS-------------------------------------
    path(
        'admin-room-requests/',
        views.admin_room_requests_view,
        name='admin-room-requests'
    ),

    # 2. approve one request
    path(
        'approve-room-request/<int:pk>/',
        views.approve_room_request_view,
        name='approve-room-request'
    ),

    # 3. reject (or delete) one request
    path(
        'reject-room-request/<int:pk>/',
        views.reject_room_request_view,
        name='reject-room-request'
    ),

    # 4. global room-availability dashboard
    path(
        'admin-room-availability/',
        views.admin_room_availability_view,
        name='admin-room-availability'
    ),
    # 2️⃣ Allow admin to delete an approved booking

]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),
    
    path(
        'patient-request-room/',
        views.patient_request_room_view,
        name='patient-request-room'
    ),

    # 2) the status page that *lists* all of your past requests:
    path(
        'patient-view-room/',
        views.patient_room_requests_view,
        name='patient-view-room'
    ),
    
    path(
        'admin/room-requests/<int:pk>/assign/',
        views.assign_room_request_view,
        name='approve-room-request'
    ),
    
    path('blog/', views.blog_view, name='blog'),
    path('patient-room/', views.patient_room, name='patient-room'),

]


# hospital/urls.py



