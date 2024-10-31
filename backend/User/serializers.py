"""
User serializers module.

This module defines serializers for the User application, including serializers for the User and UserProfile models.

Classes:
    UserProfileSerializer: Serializer for the UserProfile model.
    UserSerializer: Serializer for the User model.
    RegisterSerializer: Serializer for registering new users.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    This serializer provides a way to serialize and deserialize UserProfile instances.
    """

    class Meta:
        """
        Meta class for the UserProfileSerializer.

        This class defines the model and fields for the serializer.
        """
        model = UserProfile
        fields = ('phone_number', 'date_of_birth')

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer provides a way to serialize and deserialize User instances, including their associated UserProfile instances.
    """

    profile = UserProfileSerializer()

    class Meta:
        """
        Meta class for the UserSerializer.

        This class defines the model and fields for the serializer.
        """
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        """
        Update an existing User instance.

        This method updates the User instance with the provided validated data, including its associated UserProfile instance.

        Args:
            instance (User): The User instance to update.
            validated_data (dict): The validated data to update the User instance with.

        Returns:
            User: The updated User instance.
        """
        profile_data = validated_data.pop('profile', {})
        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update Profile fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    This serializer provides a way to serialize and deserialize data for registering new users.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        Meta class for the RegisterSerializer.

        This class defines the model and fields for the serializer.
        """
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        """
        Validate the data for registering a new user.

        This method checks that the password and password2 fields match, and that the email address is not already registered.

        Args:
            attrs (dict): The data to validate.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the data is invalid.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        return attrs

    def create(self, validated_data):
        """
        Create a new User instance.

        This method creates a new User instance with the provided validated data.

        Args:
            validated_data (dict): The validated data to create the User instance with.

        Returns:
            User: The created User instance.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
