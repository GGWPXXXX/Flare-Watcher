from django.http import HttpResponse
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from django.urls import resolve
from .views import line_webhook, send_line_message
from unittest.mock import patch
from .views import check_user_id, publish_mqtt_message, get_user_id, line_webhook
from decouple import config
from unittest.mock import patch, Mock
import json

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'flare_watcher.settings'


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
        """ Test if the line_webhook view returns 405 Method Not Allowed 
        when a GET request is made """
        response = self.client.get(self.line_webhook_url)
        self.assertEquals(response.status_code, 405)

    def test_get_user_id_POST(self):
        """ Test if the get_user_id view returns 405 Method Not Allowed 
        when a POST request is made """
        response = self.client.post(self.get_user_id_url)
        self.assertEquals(response.status_code, 405)

    def test_get_user_id_GET_without_valid_user_id(self):
        """ Test if the get_user_id view returns 200 OK when a GET request is made """
        response = self.client.get(self.get_user_id_url)
        self.assertEquals(response.status_code, 400)

    def test_get_user_id_GET_with_valid_user_id(self):
        """Test if the get_user_id view returns 200 OK when a GET request is made 
        with valid user_id"""
        response = self.client.get(
            f"/webhook/get_user_id/{self.valid_user_id}/")
        self.assertEqual(response.status_code, 200)

    def test_get_user_id_GET_with_invalid_user_id(self):
        """Test if the get_user_id view returns 400 Bad Request when a GET request is 
        made with invalid user_id"""
        response = self.client.get(
            f"/webhook/get_user_id/{self.invalid_user_id}/")
        self.assertEqual(response.status_code, 400)

    # def test_line_webhook_POST_with_valid_user_id(self):
    #     """Test if the line_webhook view returns 200 OK when a POST request is made with valid user_id"""
    #     response = self.client.post(self.line_webhook_url, {'events':
    #                                                         [{'type': 'message',
    #                                                         'source': {'userId': self.valid_user_id},
    #                                                         'message': {'text': 'UserId'}}]})
    #     self.assertEqual(response.status_code, 200)


    # @patch('requests.post')
    # def test_publish_mqtt_message(self, mock_post):
    #     """Test the publish_mqtt_message function"""
    #     # Call the function
    #     response = publish_mqtt_message("test_topic", "test_message")

    #     # Assert that the function returns a success response
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b"Success")

    #     # Assert that the function makes the expected HTTP POST request
    #     mock_post.assert_called_once_with(
    #         'https://api.line.me/v2/bot/message/push',
    #         headers={'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_CHANNEL_ACCESS_TOKEN'},
    #         data=json.dumps({"to": "test_user_id", "messages": [{"type": "text", "text": "test_message"}]})
    #     )

    # @patch('requests.post')
    # def test_line_webhook_live_data(self, mock_post):
    #     """Test the line_webhook view for live data message"""
    #     # Prepare mock data for Line webhook POST request
    #     data = {
    #         "events": [{
    #             "type": "message",
    #             "source": {"userId": "test_user_id"},
    #             "message": {"text": "Live Data"}
    #         }]
    #     }

    #     # Call the view function with mock data
    #     response = self.client.post(reverse('line_webhook'), data=json.dumps(data), content_type='application/json')

    #     # Assert that the view returns a success response
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b"Success")

    #     # Assert that the function publishes the expected MQTT message
    #     mock_post.assert_called_once_with('test_topic', 'Send live data', headers={'Content-Type': 'application/json'})

    # def test_line_webhook_default_response(self):
    #     """Test the line_webhook view for default response"""
    #     # Prepare mock data for Line webhook POST request
    #     data = {
    #         "events": [{
    #             "type": "other_event_type",
    #         }]
    #     }

    #     # Call the view function with mock data
    #     response = self.client.post(reverse('line_webhook'), data=json.dumps(data), content_type='application/json')

    #     # Assert that the view returns a default success response
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.content, b"Default response")


# class LineWebhookTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user_id = 'dummy_user_id'
#         self.access_token = config('CHANEL_ACCESS_TOKEN')
#         self.valid_body = json.dumps({
#             "events": [{
#                 "type": "message",
#                 "replyToken": "dummy_reply_token",
#                 "source": {"userId": self.user_id},
#                 "message": {"type": "text", "text": "UserId"}
#             }]
#         })
#         self.invalid_body = json.dumps({
#             "events": [{
#                 "type": "message",
#                 "replyToken": "invalid_reply_token",
#                 "source": {"userId": "invalid_user_id"},
#                 "message": {"type": "text", "text": "Invalid"}
#             }]
#         })

#     @patch('webhook_manager.views.check_user_id')
#     @patch('webhook_manager.views.get_user_id')
#     def test_line_webhook_post_valid(self, mock_get_user_id, mock_check_user_id):
#         mock_check_user_id.return_value = True
#         mock_get_user_id.return_value = HttpResponse(status=200, content="Success")

#         response = self.client.post(reverse('webhook_manager:line_webhook'),
#                                     self.valid_body, content_type='application/json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.content.decode(), 'Success')
#         mock_check_user_id.assert_called_once_with(self.user_id)
#         mock_get_user_id.assert_called_once()

#     def test_line_webhook_method_not_allowed(self):
#         response = self.client.get(reverse('webhook_manager:line_webhook'))
#         self.assertEqual(response.status_code, 405)

#     @patch('webhook_manager.views.requests.post')
#     @patch('webhook_manager.views.check_user_id')
#     def test_send_line_message(self, mock_check_user_id, mock_requests_post):
#         mock_check_user_id.return_value = True
#         response_mock = Mock()
#         response_mock.status_code = 200
#         mock_requests_post.return_value = response_mock

#         response = send_line_message(self.user_id, "Hello!")

#         self.assertEqual(response.status_code, 200)
#         mock_requests_post.assert_called_once_with(
#             "https://api.line.me/v2/bot/message/push",
#             headers={
#                 "Content-Type": "application/json",
#                 "Authorization": f"Bearer {self.access_token}"
#             },
#             data=json.dumps({
#                 "to": self.user_id,
#                 "messages": [{"type": "text", "text": "Hello!"}]
#             })
#         )

#     def test_unsupported_message_type(self):
#         body_with_unsupported_message_type = json.dumps({
#             "events": [{
#                 "type": "unsupported_type",
#                 "replyToken": "dummy_reply_token",
#                 "source": {"userId": self.user_id},
#                 "message": {"type": "image", "text": "Unsupported"}
#             }]
#         })
#         response = self.client.post(reverse('webhook_manager:line_webhook'),
#                                     body_with_unsupported_message_type, content_type='application/json')
#         # Expecting a 400 status code for unsupported message types
#         self.assertEqual(response.status_code, 400)

#     def test_exception_handling(self):
#         with patch('webhook_manager.views.json.loads', side_effect=Exception("Test Exception")):
#             response = self.client.post(reverse('webhook_manager:line_webhook'), 
#                                         self.valid_body, content_type='application/json')
#             self.assertEqual(response.status_code, 400)
#             self.assertIn("Test Exception", response.content.decode())

#     def test_invalid_user_id(self):
#         with patch('webhook_manager.views.check_user_id', return_value=False):
#             response = self.client.post(reverse('webhook_manager:line_webhook'),
#                                         self.valid_body, content_type='application/json')
#             self.assertEqual(response.status_code, 400)
#             self.assertIn("User not found", response.content.decode())
