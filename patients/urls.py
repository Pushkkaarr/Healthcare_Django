from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients.views import PatientViewSet

app_name = 'patients'

router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')

urlpatterns = [
    path('', include(router.urls)),
]
