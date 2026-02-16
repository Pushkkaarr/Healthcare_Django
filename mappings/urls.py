from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mappings.views import PatientDoctorMappingViewSet

app_name = 'mappings'

router = DefaultRouter()
router.register(r'', PatientDoctorMappingViewSet, basename='mapping')

urlpatterns = [
    path('', include(router.urls)),
]
