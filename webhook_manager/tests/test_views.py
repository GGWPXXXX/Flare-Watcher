from django.test import Client, TestCase
from django.urls import reverse
from django.test import RequestFactory
from django.core.exceptions import ValidationError
from decouple import config
import json
from webhook_manager.views import get_user_id
from webhook_manager.models import LineWebhook

class TestViews(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.fake_payload = {
            "events": [
                {
                    "type": "message",
                    "source": {
                        "userId": "1234567890"
                    },
                    "message": {
                        "text": "UserId"
                    }
                }
            ]
        }

    def test_line_webhook_post_success(self):
        response = self.client.post('/line_webhook/', data=json.dumps(self.fake_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LineWebhook.objects.count(), 1)

    def test_line_webhook_post_invalid_data(self):
        fake_payload_invalid = {
            "events": [
                {
                    "type": "message",
                    "source": {
                        "userId": "1234567890"
                    },
                    "message": {
                        "text": "InvalidMessage"
                    }
                }
            ]
        }
        response = self.client.post('/line_webhook/', data=json.dumps(fake_payload_invalid), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LineWebhook.objects.count(), 0)

    def test_line_webhook_post_error(self):
        with self.assertRaises(ValidationError):
            response = self.client.post('/line_webhook/', data=json.dumps({}), content_type='application/json')

    def test_line_webhook_get_method_not_allowed(self):
        response = self.client.get('/line_webhook/')
        self.assertEqual(response.status_code, 405)

    def test_get_user_id_success(self):
        fake_request = self.factory.get(reverse('webhook_manager:get_user_id', kwargs={'user_id': config("USER_ID")}))
        response = get_user_id(fake_request, user_id=config("USER_ID"))
        self.assertEqual(response.status_code, 200)

    def test_get_user_id_failure(self):
        with self.assertRaises(KeyError):
            fake_request = self.factory.get(reverse('webhook_manager:get_user_id', kwargs={'user_id': '1234567890'}))
            get_user_id(fake_request, user_id='1234567890_invalid')
