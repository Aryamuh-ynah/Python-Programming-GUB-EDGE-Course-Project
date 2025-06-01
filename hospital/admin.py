from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails
from .models import Room, RoomRequest

# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type',)

@admin.register(RoomRequest)
class RoomRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'room_type', 'status', 'requested_at', 'approved_at')
    list_filter  = ('status','room_type')
    actions      = ('approve_requests',)

    def approve_requests(self, request, queryset):
        updated = queryset.filter(status=False).update(
            status=True,
            approved_at=timezone.now()
        )
        self.message_user(request, f"{updated} request(s) approved.")
    approve_requests.short_description = "Mark selected requests as approved"