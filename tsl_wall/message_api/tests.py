from django.contrib.auth.models import User
from django.test import TestCase
import json
from message_api.models import Message

"""
Tests for Message API
"""


class MessageAPITest(TestCase):

    def setUp(self):
        Message.objects.create(content="m1", username="test", user_id=1)
        Message.objects.create(content="m2", username="test", user_id=1)
        User.objects.create_user(username="test", password="qwer1234")
        client = self.client
        client.post('/api/users/login/', {'username': 'test', 'password': 'qwer1234'})


    def test_get_message(self):
        client = self.client

        # Test case with get
        response = client.get('/api/messages/')
        self.assertEqual(response.status_code, 200)

        response = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response), 2)

    def test_post_message(self):
        client = self.client

        # test case with auth user
        response = client.post('/api/messages/', {'content': "from api", 'username': 'test', 'user_id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.all().count(), 3)

        # test case with unauth user
        client.post('/api/users/logout/', {'username': 'test', 'user_id': 1})
        response = client.post('/api/messages/', {'content': "from api", 'username': 'test', 'user_id': 1})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Message.objects.all().count(), 3)

