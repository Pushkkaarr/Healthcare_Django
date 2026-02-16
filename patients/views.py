from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from patients.models import Patient
from patients.serializers import PatientSerializer, PatientCreateUpdateSerializer


class IsPatientOwner(permissions.BasePermission):
    """Custom permission to check if user is the patient"""
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet for Patient CRUD operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientSerializer
    
    def get_queryset(self):
        """Return patients for the authenticated user"""
        return Patient.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return PatientCreateUpdateSerializer
        return PatientSerializer
    
    def perform_create(self, serializer):
        """Create patient with authenticated user"""
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create a new patient"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Patient created successfully',
                'data': PatientSerializer(serializer.instance).data
            },
            status=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        """List all patients for authenticated user"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'count': len(serializer.data),
                'patients': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific patient"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """Update a patient (full update)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'message': 'Patient updated successfully',
                'data': PatientSerializer(serializer.instance).data
            },
            status=status.HTTP_200_OK
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update a patient"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'message': 'Patient updated successfully',
                'data': PatientSerializer(serializer.instance).data
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a patient"""
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Patient deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
