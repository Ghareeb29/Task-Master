"""
User views module.

This module defines views for handling user registration and profile retrieval.

Classes:
    RegisterView: View for handling user registration.
    UserProfileView: View for handling user profile retrieval.
"""
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer

@extend_schema_view(
    post=extend_schema(description='Register a new user', request=RegisterSerializer, responses={201: UserSerializer}),
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@extend_schema_view(
    get=extend_schema(description='Retrieve the profile of the currently authenticated user', responses={200: UserSerializer}),
    patch=extend_schema(description='Update the profile of the currently authenticated user', request=UserSerializer, responses={200: UserSerializer}),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
