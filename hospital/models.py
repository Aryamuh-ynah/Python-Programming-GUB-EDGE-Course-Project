from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

from django.core.validators import RegexValidator  # Add this at the top

bd_phone_validator = RegexValidator(
    regex=r'^01[3-9]\d{8}$',
    message='Enter a valid Bangladeshi phone number (e.g., 01712345678) \n-> It should start with 01 and be followed by 9 digits.',
)

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(
        max_length=11,
        null=True,
        validators=[bd_phone_validator])
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(
        max_length=11,
        null=True,
        validators=[bd_phone_validator])
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):

    description   = models.TextField()
    status        = models.BooleanField(default=False)
    doctorId = models.PositiveIntegerField(null=True, blank=True)
    patientId     = models.IntegerField(null=True, blank=True)
    doctorName    = models.CharField(max_length=200)
    patientName   = models.CharField(max_length=200)
    appointment_datetime = models.DateTimeField(
    verbose_name="Appointment date & time",
    null=True,
    blank=True,
    )



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False, default=0)

    roomCharge=models.PositiveIntegerField(null=False, default=0)
    medicineCost=models.PositiveIntegerField(null=False, default=0)
    doctorFee=models.PositiveIntegerField(null=False, default=0)
    OtherCharge=models.PositiveIntegerField(null=False, default=0)
    total=models.PositiveIntegerField(null=False, default=0)


class Room(models.Model):
    ICU     = "ICU"
    GENERAL = "General"
    PRIVATE = "Private"
    ROOM_TYPE_CHOICES = [
        (ICU,     "ICU"),
        (GENERAL, "General"),
        (PRIVATE, "Private"),
    ]

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPE_CHOICES,
        unique=True,
    )
    # how many beds of this type exist
    capacity = models.PositiveIntegerField(
        default=1,
        help_text="Total beds of this type in hospital"
    )
    
    # optional: track total capacity, etc.
    def __str__(self):
        return self.room_type


class RoomRequest(models.Model):
    PENDING  = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    # 2) Build a choices tuple
    STATUS_CHOICES = [
        (PENDING,  'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    patient      = models.ForeignKey(
        'Patient',                # your Patient model
        on_delete=models.CASCADE
    )
    room_type    = models.CharField(
        max_length=20,
        choices=Room.ROOM_TYPE_CHOICES,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    assigned_room = models.CharField(
        max_length=10,
        blank=True,
        help_text="Room number assigned by admin upon approval"
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at  = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When admin approved"
    )
    start_datetime  = models.DateTimeField(
        null=True,             # allow NULL in the database
        blank=True,            # allow empty in forms
    )
    # → for how many hours
    duration_hours  = models.PositiveIntegerField(default=24)

    def __str__(self):
        return f"{self.patient.get_name} → {self.room_type} ({'OK' if self.status else 'Pending'})"