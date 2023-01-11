from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class AuthViewsTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.dummy_username = 'username'
        self.dummy_password = 'password'
        self.dummy_email = 'test@email.com'

    def createUser(self, username, password):
        user = User.objects.create_user(username=username, password=password)
        return user

    def test_register_view_valid_data(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

        data = {
            'username': self.dummy_username,
            'email': self.dummy_email,
            'password': self.dummy_password
        }
        response = self.client.post('/api/auth/register/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(users.count(), 1)
        new_user = users.first()
        self.assertEqual(new_user.username, self.dummy_username)
        self.assertEqual(new_user.email, self.dummy_email)

    def test_register_view_invalid_data(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

        data = {'password': self.dummy_password}
        response = self.client.post('/api/auth/register/', data=data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertTrue('username' in response_data.keys())
        self.assertEqual(users.count(), 0)

        data.pop('password')
        data.update({'username': self.dummy_username})
        response = self.client.post('/api/auth/register/', data=data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertTrue('password' in response_data.keys())
        self.assertEqual(users.count(), 0)

    def test_login_view(self):
        data = {
            'username': self.dummy_username,
            'password': self.dummy_password
        }

        # Test unregistered user
        response = self.client.post('/api/auth/login/', data=data)
        self.assertEqual(response.status_code, 401)
        response_data = response.json()
        error_message = 'No active account found with the given credentials'
        self.assertEqual(response_data['detail'], error_message)

        # Test registered user
        self.createUser(**data)
        response = self.client.post('/api/auth/login/', data=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue('access' in response_data.keys())
        self.assertTrue('refresh' in response_data.keys())

    def test_login_refresh_view(self):
        data = {
            'username': self.dummy_username,
            'password': self.dummy_password
        }

        self.createUser(**data)
        login_response = self.client.post('/api/auth/login/', data=data)
        self.assertEqual(login_response.status_code, 200)
        login_response_data = login_response.json()
        access_key = login_response_data['access']
        refresh_key = login_response_data['refresh']

        refresh_response = self.client.post('/api/auth/login/refresh/',
                                    data={'refresh': refresh_key})
        self.assertEqual(refresh_response.status_code, 200)
        refresh_response_data = refresh_response.json()
        new_access_key = refresh_response_data['access']
        self.assertNotEqual(new_access_key, access_key)
