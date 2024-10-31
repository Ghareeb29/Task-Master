from django.db.utils import IntegrityError
from django.test import TestCase
from User.serializers import UserSerializer, RegisterSerializer, UserProfileSerializer
from User.models import UserProfile
from rest_framework.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import json


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_creation(self):
        """Test that a UserProfile is automatically created when a User is created"""
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

    def test_profile_str_representation(self):
        """Test the string representation of UserProfile"""
        profile = self.user.profile
        self.assertEqual(str(profile), 'testuser')

    def test_profile_fields(self):
        """Test that profile fields can be updated"""
        profile = self.user.profile
        profile.phone_number = '1234567890'
        profile.date_of_birth = '1990-01-01'
        profile.save()
        
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.phone_number, '1234567890')
        self.assertEqual(str(updated_profile.date_of_birth), '1990-01-01')

    def test_cascade_deletion(self):
        """Test that UserProfile is deleted when User is deleted"""
        profile_id = self.user.profile.id
        self.user.delete()
        self.assertFalse(UserProfile.objects.filter(id=profile_id).exists())

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'profile': {
                'phone_number': '1234567890',
                'date_of_birth': '1990-01-01'
            }
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )

    def test_user_serialization(self):
        """Test that a user can be serialized"""
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertEqual(serializer.data['email'], 'test@example.com')

    def test_profile_included_in_serialization(self):
        """Test that profile data is included in user serialization"""
        profile = self.user.profile
        profile.phone_number = '1234567890'
        profile.save()
        
        serializer = UserSerializer(self.user)
        self.assertIn('profile', serializer.data)
        self.assertEqual(serializer.data['profile']['phone_number'], '1234567890')

class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }

    def test_valid_registration(self):
        """Test registration with valid data"""
        serializer = RegisterSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test registration with mismatched passwords"""
        payload = self.valid_payload.copy()
        payload['password2'] = 'wrongpass'
        serializer = RegisterSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_duplicate_email(self):
        """Test registration with duplicate email"""
        User.objects.create_user(
            username='existinguser',
            email=self.valid_payload['email'],
            password='testpass123'
        )
        serializer = RegisterSerializer(data=self.valid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_valid_registration(self):
        """Test successful user registration"""
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_invalid_registration_missing_field(self):
        """Test registration with missing required field"""
        payload = self.valid_payload.copy()
        del payload['email']
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration_weak_password(self):
        """Test registration with weak password"""
        payload = self.valid_payload.copy()
        payload['password'] = '123'
        payload['password2'] = '123'
        response = self.client.post(
            self.register_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile_url = reverse('user_profile')
        self.client.force_authenticate(user=self.user)

    def test_get_own_profile(self):
        """Test retrieving own profile"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        """Test updating profile information"""
        payload = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'profile': {
                'phone_number': '9876543210',
                'date_of_birth': '1995-01-01'
            }
        }
        response = self.client.put(
            self.profile_url,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.profile.phone_number, '9876543210')

    def test_unauthorized_access(self):
        """Test accessing profile without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserAuthenticationFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
        self.profile_url = reverse('user_profile')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_full_authentication_flow(self):
        """Test complete user registration, login, and profile access flow"""
        # 1. Register new user
        register_response = self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # 2. Login with new user
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        login_response = self.client.post(
            self.login_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

        # 3. Access profile with token
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        profile_response = self.client.get(self.profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['username'], self.user_data['username'])

    def test_profile_update_flow(self):
        """Test profile update flow after registration and login"""
        # Register and login
        self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        login_response = self.client.post(
            self.login_url,
            data={'username': self.user_data['username'], 'password': self.user_data['password']},
            content_type='application/json'
        )
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Update profile
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'profile': {
                'phone_number': '9876543210',
                'date_of_birth': '1995-01-01'
            }
        }
        update_response = self.client.put(
            self.profile_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        # Verify updates
        profile_response = self.client.get(self.profile_url)
        self.assertEqual(profile_response.data['first_name'], 'Updated')
        self.assertEqual(profile_response.data['profile']['phone_number'], '9876543210')
