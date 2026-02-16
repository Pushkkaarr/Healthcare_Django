from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from mappings.models import PatientDoctorMapping
from patients.models import Patient
from mappings.serializers import PatientDoctorMappingSerializer, PatientDoctorMappingCreateUpdateSerializer


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """ViewSet for PatientDoctorMapping CRUD operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientDoctorMappingSerializer
    queryset = PatientDoctorMapping.objects.all()
    filterset_fields = ['status', 'patient', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    ordering_fields = ['assignment_date', 'status']
    ordering = ['-assignment_date']
    
    def get_serializer_class(self):
        """Use different serializer for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return PatientDoctorMappingCreateUpdateSerializer
        return PatientDoctorMappingSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new mapping"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Doctor assigned to patient successfully',
                'data': PatientDoctorMappingSerializer(serializer.instance).data
            },
            status=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        """List all mappings"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'count': self.paginator.count,
                'mappings': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'count': len(serializer.data),
                'mappings': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific mapping"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """Update a mapping (full update)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'message': 'Mapping updated successfully',
                'data': PatientDoctorMappingSerializer(serializer.instance).data
            },
            status=status.HTTP_200_OK
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update a mapping"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'message': 'Mapping updated successfully',
                'data': PatientDoctorMappingSerializer(serializer.instance).data
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a mapping"""
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Mapping deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get all doctors assigned to a specific patient"""
        patient_id = request.query_params.get('patient_id')
        
        if not patient_id:
            return Response(
                {'error': 'patient_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = self.get_serializer(mappings, many=True)
        
        return Response(
            {
                'patient_id': patient_id,
                'doctor_count': len(serializer.data),
                'doctors': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def statuses(self, request):
        """Get all available statuses"""
        statuses = [
            {'id': choice[0], 'name': choice[1]} 
            for choice in PatientDoctorMapping.STATUS_CHOICES
        ]
        return Response(statuses, status=status.HTTP_200_OK)
