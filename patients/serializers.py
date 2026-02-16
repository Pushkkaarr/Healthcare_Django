from rest_framework import serializers
from patients.models import Patient
from auth_app.serializers import CustomUserSerializer


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""
    
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'blood_type', 'address', 'city',
            'state', 'postal_code', 'medical_history', 'allergies',
            'emergency_contact', 'emergency_phone', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_phone(self, value):
        """Validate phone number format"""
        if not value.replace('-', '').replace('+', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits and optional + or - characters.")
        return value
    
    def validate_postal_code(self, value):
        """Validate postal code format"""
        if not value.replace('-', '').isalnum():
            raise serializers.ValidationError("Postal code must contain only alphanumeric characters and optional hyphens.")
        return value


class PatientCreateUpdateSerializer(PatientSerializer):
    """Serializer for creating and updating patients"""
    
    class Meta(PatientSerializer.Meta):
        read_only_fields = ['id', 'created_at', 'updated_at']
