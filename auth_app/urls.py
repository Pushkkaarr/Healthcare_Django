from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from auth_app.views import RegisterView, LoginView, UserProfileView

app_name = 'auth_app'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
