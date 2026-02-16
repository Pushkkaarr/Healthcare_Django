from rest_framework import serializers
from doctors.models import Doctor
from auth_app.serializers import CustomUserSerializer


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model"""
    
    user = CustomUserSerializer(read_only=True)
    get_specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    get_gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'gender', 'get_gender_display', 'specialization', 'get_specialization_display',
            'license_number', 'hospital_affiliation', 'experience_years',
            'consultation_fee', 'bio', 'office_address', 'office_phone',
            'available_days', 'available_hours', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_phone(self, value):
        """Validate phone number format"""
        if not value.replace('-', '').replace('+', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits and optional + or - characters.")
        return value
    
    def validate_email(self, value):
        """Validate email is unique (except when updating)"""
        if self.instance is None:
            if Doctor.objects.filter(email=value).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        else:
            if Doctor.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        return value
    
    def validate_license_number(self, value):
        """Validate license number is unique"""
        if self.instance is None:
            if Doctor.objects.filter(license_number=value).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        else:
            if Doctor.objects.filter(license_number=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        return value


class DoctorCreateUpdateSerializer(DoctorSerializer):
    """Serializer for creating and updating doctors"""
    
    class Meta(DoctorSerializer.Meta):
        read_only_fields = ['id', 'created_at', 'updated_at']
