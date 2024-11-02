from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

class RegistrationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')  # Adjust if your URL pattern name is different

    def test_register_user_successfully(self):
        """
        Ensure we can register a new user with valid data.
        """
        data = {
            "username": "newuser",
            "password": "strongpassword123",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.register_url, data, format='json')

        # Check if registration was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["username"], data["username"])
        self.assertEqual(response.data["user"]["email"], data["email"])

        # Verify user creation in the database
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_user_missing_fields(self):
        """
        Ensure registration fails if required fields are missing.
        """
        data = {
            "username": "newuser",
            "email": "newuser@example.com"  # Missing password field
        }
        response = self.client.post(self.register_url, data, format='json')

        # Check if we receive a bad request status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  # Expect an error for missing password

    def test_register_user_with_existing_username(self):
        """
        Ensure registration fails if username already exists.
        """
        User.objects.create_user(username="existinguser", password="password123", email="existing@example.com")

        data = {
            "username": "existinguser",
            "password": "anotherpassword123",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.register_url, data, format='json')

        # Check if we receive a bad request status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)  # Expect an error about username being taken


class LoginTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')  # Adjust if your URL pattern name is different
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="test@example.com")

    def test_login_user_successfully(self):
        """
        Ensure a user can log in with valid credentials and receives access and refresh tokens.
        """
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, data, format='json')

        # Checking if login was successful.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertEqual(response.data["message"], "User authenticated successfully")

    def test_login_user_invalid_credentials(self):
        """
        Ensure login fails with invalid credentials.
        """
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format='json')

        # Check if we receive an unauthorized status
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials")

    def test_login_user_missing_fields(self):
        """
        Ensure login fails if required fields are missing.
        """
        data = {
            "username": "testuser"  # Missing password field
        }
        response = self.client.post(self.login_url, data, format='json')

        # Check if we receive a bad request status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)  # Expect an error about missing password