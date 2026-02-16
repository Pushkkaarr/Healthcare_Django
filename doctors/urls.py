from django.urls import path, include
from rest_framework.routers import DefaultRouter
from doctors.views import DoctorViewSet

app_name = 'doctors'

router = DefaultRouter()
router.register(r'', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('', include(router.urls)),
]
