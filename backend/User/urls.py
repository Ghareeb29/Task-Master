from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserProfileView

router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')
router.register(r'profile', UserProfileView, basename='profile')

urlpatterns = [
    path('api/auth/', include(router.urls)),
]
