from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from User.models import UserProfile


class UserRegistrationTests(APITestCase):
    def test_valid_registration(self):
        """Test user registration with valid data"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(reverse('auth_register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_invalid_password_match(self):
        """Test registration with non-matching passwords"""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "password2": "DifferentPass123!",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(reverse('auth_register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_duplicate_email(self):
        """Test registration with an existing email"""
        User.objects.create_user(username="existing", email="test@example.com", password="pass123")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        response = self.client.post(reverse('auth_register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Test retrieving user profile"""
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        """Test updating user profile"""
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "profile": {
                "phone_number": "1234567890",
                "date_of_birth": "1990-01-01"
            }
        }
        response = self.client.put(reverse('user_profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['profile']['phone_number'], '1234567890')

    def test_unauthorized_access(self):
        """Test accessing profile without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
