from django import forms
from django.contrib.auth.models import User
from . import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import socket
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import dns.resolver
from django.utils import timezone
from datetime import datetime
import pytz
#for admin signup
class AdminSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label="Email Address", required=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        # 1) validate syntax
        validate_email(email)

        # 2) MX lookup
        domain = email.split('@')[1]
        try:
            dns.resolver.resolve(domain, 'MX')
        except dns.resolver.NXDOMAIN:
            raise forms.ValidationError("❌ That domain doesn’t exist.")
        except dns.resolver.NoAnswer:
            raise forms.ValidationError("❌ That domain has no mail servers (MX records).")

        # 3) duplicates
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("❌ That email is already registered.")

        return email
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
            
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
            
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one number.")
            
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        

#for student related form
class DoctorUserForm(forms.ModelForm):
    email = forms.EmailField(label="Email Address", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 1) basic format check
        try:
            validate_email(email)
        except DjangoValidationError:
            raise forms.ValidationError("❌ Enter a valid email address.")
        # 2) DNS lookup on the domain part
        domain = email.split('@')[-1]
        try:
            socket.getaddrinfo(domain, None)
        except socket.gaierror:
            raise forms.ValidationError("❌ Email domain does not exist.")
        # 3) uniqueness
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("❌ That email is already in use.")
        return email
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match")

            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not re.search(r'[A-Z]', password):
                self.add_error('password', "Password must contain at least one uppercase letter.")
            if not re.search(r'[a-z]', password):
                self.add_error('password', "Password must contain at least one lowercase letter.")
            if not re.search(r'\d', password):
                self.add_error('password', "Password must contain at least one number.")
            if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
                self.add_error('password', "Password must contain at least one special character.")
    
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']




class PatientUserForm(forms.ModelForm):
    email = forms.EmailField(label="Email Address", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match")

            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if not re.search(r'[A-Z]', password):
                self.add_error('password', "Password must contain at least one uppercase letter.")
            if not re.search(r'[a-z]', password):
                self.add_error('password', "Password must contain at least one lowercase letter.")
            if not re.search(r'\d', password):
                self.add_error('password', "Password must contain at least one number.")
            if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
                self.add_error('password', "Password must contain at least one special character.")
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except DjangoValidationError:
            raise forms.ValidationError("❌ Enter a valid email address.")
        domain = email.split('@')[1]
        try:
            socket.getaddrinfo(domain, None)
        except socket.gaierror:
            raise forms.ValidationError("❌ Email domain does not exist.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("❌ That email is already in use.")
        return email

class PatientForm(forms.ModelForm):
   
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic']

from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class CustomAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # This is called after successful credential check
        if not user.is_active:
            # User exists but isn’t active yet
            raise ValidationError(
                "❗ Please verify your email address before logging in.",
                code='inactive',
            )
        # Otherwise allow login as normal
        super().confirm_login_allowed(user)



class AppointmentForm(forms.ModelForm):

    doctorId   = forms.ModelChoiceField(queryset=models.Doctor.objects.filter(status=True),
                                        empty_label="Doctor Name and Department",
                                        to_field_name="user_id")
    patientId  = forms.ModelChoiceField(queryset=models.Patient.objects.filter(status=True),
                                        empty_label="Patient Name and Symptoms",
                                        to_field_name="user_id")
    appointment_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type':'datetime-local','class':'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta:
        model  = models.Appointment
        fields = ['description','appointment_datetime','status']


from django.forms.widgets import DateTimeInput
from .models import Appointment

class PatientAppointmentForm(forms.ModelForm):
    appointment_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'type':'datetime-local','class':'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    doctorId = forms.ModelChoiceField(
        queryset=models.Doctor.objects.filter(status=True),
        empty_label="Select a doctor…",
        to_field_name="user_id",
        widget=forms.Select(attrs={'class':'form-select'})
    )
    class Meta:
        model  = models.Appointment
        fields = ['description','appointment_datetime','status']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tell Django how to parse the incoming datetime-local string
        self.fields['appointment_datetime'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean_appointment_datetime(self):
        dt = self.cleaned_data['appointment_datetime']
        if dt < timezone.now():
            raise forms.ValidationError("❌ You can only book for a future date/time.")
        return dt



class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


from django import forms
from .models import RoomRequest, Room
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.models import F, Value, ExpressionWrapper, DateTimeField

class RoomRequestForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        label="Start (date & time)",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    duration_hours = forms.IntegerField(
        label="Duration (Days)",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="Number of hours to book"
    )

    class Meta:
        model = RoomRequest
        fields = ['room_type', 'start_datetime', 'duration_hours']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'form-select'})
        }

    def clean_start_datetime(self):
        """
        Prevent booking in the past.
        """
        start_dt = self.cleaned_data.get('start_datetime')
        if start_dt and start_dt < timezone.now():
            raise ValidationError("❌ Start date/time cannot be in the past.")
        return start_dt

    def clean(self):
        cd = super().clean()
        rt_code = cd.get('room_type')
        start   = cd.get('start_datetime')
        hrs     = cd.get('duration_hours')

        if not (rt_code and start and hrs):
            return cd

        # compute the new booking end
        end = start + timedelta(hours=hrs)

        # count any requests that start inside your window
        overlaps = RoomRequest.objects.filter(
            room_type=rt_code,
            status=RoomRequest.APPROVED,
            start_datetime__lt=end,
            start_datetime__gt=start
        )

        # look up the capacity from the real Room object
        from .models import Room
        room = Room.objects.get(room_type=rt_code)

        if overlaps.count() >= room.capacity:
            raise ValidationError(f"No '{room.get_room_type_display()}' rooms free.")

        return cd
    
class AssignRoomForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        fields = ['assigned_room']
        widgets = {
            'assigned_room': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 101A'
            }),
        }
        labels = {
            'assigned_room': 'Room Number',
        }