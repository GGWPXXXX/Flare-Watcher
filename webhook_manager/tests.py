from django.test import Client, TestCase
from django.urls import reverse
from django.urls import resolve
from .views import line_webhook
from .views import get_user_id
from decouple import config


class TestUrls(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.line_webhook_url = reverse('webhook_manager:line_webhook')
        cls.get_user_id_url = reverse(
            'webhook_manager:get_user_id', args=['user_id'])
        cls.valid_user_id = config('USER_ID')
        cls.invalid_user_id = '1234567890'

    def test_line_webhook_url_resolves(self):
        """ Test if the line_webhook view resolves the line_webhook_url """
        self.assertEqual(resolve(self.line_webhook_url).func, line_webhook)

    def test_get_user_id_url_resolves(self):
        """ Test if the get_user_id view resolves the get_user_id_url """
        self.assertEqual(resolve(self.get_user_id_url).func, get_user_id)

    def test_line_webhook_GET(self):
        """ Test if the line_webhook view returns 405 Method Not Allowed when a GET request is made """
        response = self.client.get(self.line_webhook_url)
        self.assertEquals(response.status_code, 405)

    def test_get_user_id_POST(self):
        """ Test if the get_user_id view returns 405 Method Not Allowed when a POST request is made """
        response = self.client.post(self.get_user_id_url)
        self.assertEquals(response.status_code, 405)

    def test_get_user_id_GET_without_valid_user_id(self):
        """ Test if the get_user_id view returns 200 OK when a GET request is made """
        response = self.client.get(self.get_user_id_url)
        self.assertEquals(response.status_code, 400)

    def test_get_user_id_GET_with_valid_user_id(self):
        """Test if the get_user_id view returns 200 OK when a GET request is made with valid user_id"""
        response = self.client.get(
            f"/webhook/get_user_id/{self.valid_user_id}/")
        self.assertEqual(response.status_code, 200)

    def test_get_user_id_GET_with_invalid_user_id(self):
        """Test if the get_user_id view returns 400 Bad Request when a GET request is made with invalid user_id"""
        response = self.client.get(
            f"/webhook/get_user_id/{self.invalid_user_id}/")
        self.assertEqual(response.status_code, 400)
