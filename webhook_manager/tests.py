from django.test import Client, TestCase
from django.urls import reverse
from django.urls import resolve
from .views import line_webhook
from .views import get_user_id

class TestUrls(TestCase):
    
    @classmethod
    def setUp(cls):
        cls.client = Client()
        cls.line_webhook_url = reverse('webhook_manager:line_webhook')
        cls.get_user_id_url = reverse('webhook_manager:get_user_id', args=['user_id'])
        
    def test_line_webhook_url_resolves(self):
        self.assertEqual(resolve(self.line_webhook_url).func, line_webhook)
        
    def test_get_user_id_url_resolves(self):
        self.assertEqual(resolve(self.get_user_id_url).func, get_user_id)
        
    def test_line_webhook_GET(self):
        response = self.client.get(self.line_webhook_url)
        self.assertEquals(response.status_code, 405)
