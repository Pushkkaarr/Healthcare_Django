from django.contrib import admin
from doctors.models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'specialization', 'license_number', 'experience_years', 'is_active', 'created_at')
    list_filter = ('specialization', 'gender', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'license_number', 'specialization')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'gender')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'license_number', 'experience_years', 'hospital_affiliation', 'consultation_fee', 'bio')
        }),
        ('Office Details', {
            'fields': ('office_address', 'office_phone', 'available_days', 'available_hours')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def get_full_name(self, obj):
        return f"Dr. {obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Name'
