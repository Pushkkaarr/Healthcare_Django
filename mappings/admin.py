from django.contrib import admin
from mappings.models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'status', 'assignment_date', 'updated_at')
    list_filter = ('status', 'assignment_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')
    ordering = ('-assignment_date',)
    readonly_fields = ('assignment_date', 'updated_at')
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('patient', 'doctor', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Dates', {
            'fields': ('assignment_date', 'updated_at')
        }),
    )
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}"
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.first_name} {obj.doctor.last_name}"
    get_doctor_name.short_description = 'Doctor'
