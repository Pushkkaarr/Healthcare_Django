from rest_framework import serializers
from mappings.models import PatientDoctorMapping
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """Serializer for PatientDoctorMapping model"""
    
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    get_status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'patient_id', 'doctor', 'doctor_id',
            'assignment_date', 'status', 'get_status_display', 'notes', 'updated_at'
        ]
        read_only_fields = ['id', 'assignment_date', 'updated_at', 'patient', 'doctor']
    
    def validate(self, data):
        """Validate that patient and doctor exist and check for duplicates"""
        from patients.models import Patient
        from doctors.models import Doctor
        
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found.")
        
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            raise serializers.ValidationError("Doctor not found.")
        
        # Check if mapping already exists
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This patient is already assigned to this doctor.")
        
        data['patient'] = patient
        data['doctor'] = doctor
        return data
    
    def create(self, validated_data):
        """Create mapping with patient and doctor"""
        patient = validated_data.pop('patient')
        doctor = validated_data.pop('doctor')
        validated_data.pop('patient_id', None)
        validated_data.pop('doctor_id', None)
        
        mapping = PatientDoctorMapping.objects.create(
            patient=patient,
            doctor=doctor,
            **validated_data
        )
        return mapping


class PatientDoctorMappingCreateUpdateSerializer(PatientDoctorMappingSerializer):
    """Serializer for creating and updating mappings"""
    
    class Meta(PatientDoctorMappingSerializer.Meta):
        read_only_fields = ['id', 'assignment_date', 'updated_at', 'patient', 'doctor']
