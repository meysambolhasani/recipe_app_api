from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """ Test the users API (public) """

    def setUp(self):
        self.client = APIClient()


    def Test_create_valid_user_success(self):
        """ Test creating user with valid payload is successfull """

        payload = {
            'email': 'mytest@me.com',
            'password': 'mytestpass',
            'name': 'Test Name'
        }
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_passeord(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
            """ Test creating a user that already exists fails """

            payload = {'email': 'mytest@me.com', 'password': 'mytestpass'}
            create_user(**payload)
            response = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
            """ Test that the password must be more than 8 characters """

            payload = {'email': 'mytest@me.com', 'password': 'pw'}
            response = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            user_exists = get_user_model().objects.filter(
                email=payload['email']
            ).exists()
            self.assertFalse(user_exists)

    def test_create_token_for_user(self):
            """ Test that a token is created for user """
            payload = {'email': 'mytest@me.com', 'password': 'mytestpass'}
            create_user(**payload)
            response = self.client.post(TOKEN_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('token', response.data)

    def test_create_token_invalid_credential(self):
            """ Test that token  is not created if invalid credentials are given"""

            create_user(email='mytest@me.com', password='mytestpass')
            payload = {'email': 'mytest@me.com', 'password': 'wrongpass'}
            response = self.client.post(TOKEN_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn('token', response.data)

    def test_create_token_no_user(self):
            """ Test that token  is not created if user  doesn't exist"""

            payload = {'email': 'mytest@me.com', 'password': 'mytestpass'}
            response = self.client.post(TOKEN_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn('token', response.data)

    def test_create_token_missing_field(self):
            """ Test that email and password is required """

            payload = {'email': 'mytest', 'password': ''}
            response = self.client.post(TOKEN_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn('token', response.data)