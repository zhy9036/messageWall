from django.contrib.auth.models import User
from django.test import TestCase


"""
Tests for User API
"""
class UserAPITest(TestCase):

    def setUp(self):
        User.objects.create_user(username="test", password="qwer1234")

    def test_login(self):
        client = self.client

        # Test case with correct username password
        response = client.post('/api/users/login/', {'username': 'test', 'password': 'qwer1234'})
        self.assertEqual(response.status_code, 200)

        # Test case with wrong username password
        response = client.post('/api/users/login/', {'username': 'non_exist', 'password': 'none'})
        self.assertEqual(response.status_code, 403)

    def test_register(self):

        client = self.client

        # Test case with the username that is already token
        response = client.post('/api/users/', {'username': 'test', 'password': 'qwer1234', 'email': 'asdf'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.all().count(), 1)

        # Test cases with lack of information
        response = client.post('/api/users/', {})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(User.objects.all().count(), 1)

        response = client.post('/api/users/', {'username': 'test1', 'email': 'asdf'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.all().count(), 1)

        response = client.post('/api/users/', {'password': 'qwer1234'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(User.objects.all().count(), 1)

        response = client.post('/api/users/', {'username': 'test1', 'password': 'qwer1234'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(User.objects.all().count(), 1)

        # Test case with wrong email format
        response = client.post('/api/users/', {'username': 'test1', 'password': 'qwer1234', 'email': 'asdf'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.all().count(), 1)

        # Test case with correct information
        response = client.post('/api/users/', {'username': 'test1', 'password': 'qwer1234', 'email': 'asdf@a.com'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.all().count(), 2)

    def test_logout(self):
        client = self.client

        # Test case with already logged in user
        client.post('/api/users/login/', {'username': 'test', 'password': 'qwer1234'})
        response = client.post('/api/users/logout/', {'username': 'test', 'user_id': 1})
        self.assertEqual(response.status_code, 200)

        # Test case with non logged in user
        response = client.post('/api/users/logout/', {'username': 'random', 'user_id': 1})
        self.assertEqual(response.status_code, 403)

