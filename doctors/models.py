from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Doctor(models.Model):
    """Model for doctor information"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('GP', 'General Practitioner'),
        ('CARD', 'Cardiologist'),
        ('DERM', 'Dermatologist'),
        ('NEURO', 'Neurologist'),
        ('ORTHO', 'Orthopedic'),
        ('PEDI', 'Pediatrician'),
        ('OB-GYN', 'Obstetrics & Gynecology'),
        ('ENT', 'ENT Specialist'),
        ('ONCO', 'Oncologist'),
        ('PSY', 'Psychiatrist'),
        ('OTHER', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    hospital_affiliation = models.CharField(max_length=200, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    office_address = models.TextField(blank=True, null=True)
    office_phone = models.CharField(max_length=15, blank=True, null=True)
    available_days = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Mon, Tue, Wed, etc.")
    available_hours = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 9AM-5PM")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['specialization']),
            models.Index(fields='-created_at'),
        ]
