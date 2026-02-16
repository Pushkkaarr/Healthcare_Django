from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer, DoctorCreateUpdateSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    """ViewSet for Doctor CRUD operations"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filterset_fields = ['specialization', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'specialization']
    ordering_fields = ['first_name', 'last_name', 'experience_years', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializer for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return DoctorCreateUpdateSerializer
        return DoctorSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new doctor"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Doctor created successfully',
                'data': DoctorSerializer(serializer.instance).data
            },
            status=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        """List all doctors"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'count': self.paginator.count,
                'doctors': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'count': len(serializer.data),
                'doctors': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific doctor"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """Update a doctor (full update)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'message': 'Doctor updated successfully',
                'data': DoctorSerializer(serializer.instance).data
            },
            status=status.HTTP_200_OK
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update a doctor"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                'message': 'Doctor updated successfully',
                'data': DoctorSerializer(serializer.instance).data
            },
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a doctor"""
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Doctor deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=['get'])
    def specializations(self, request):
        """Get all available specializations"""
        specializations = [
            {'id': choice[0], 'name': choice[1]} 
            for choice in Doctor.SPECIALIZATION_CHOICES
        ]
        return Response(specializations, status=status.HTTP_200_OK)
