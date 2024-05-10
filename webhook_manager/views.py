from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
import requests
from decouple import config
from .models import LineWebhook
from django.test.client import RequestFactory
import paho.mqtt.client as mqtt

CHANEL_ACCESS_TOKEN = config('CHANEL_ACCESS_TOKEN')


@csrf_exempt
def line_webhook(request):
    """ Webhook for Line messaging API """
    factory = RequestFactory()
    if request.method == "POST":
        try:
            # create json object from the request body
            data = json.loads(request.body.decode("utf-8"))
            event_type = data['events'][0]['type']
            if event_type == "message":

                user_id = data['events'][0]['source']['userId']
                message = data['events'][0]['message']['text']
                if not check_user_id(user_id):
                    return HttpResponse(status=400, content="User not found")
                if user_id and message == 'UserId' and check_user_id(user_id):
                    LineWebhook.objects.create(
                        user_id=user_id,
                        event_type=event_type,
                    )
                    if config('DEPLOYMENT', cast=bool):
                        # create a fake GET request to call get_user_id view
                        fake_request = factory.get(
                            reverse('webhook_manager:get_user_id', kwargs={'user_id': user_id}))
                        response = get_user_id(fake_request, user_id)
                        return response
                    return get_user_id(request, user_id)
                elif message == 'Live Data' and check_user_id(user_id):
                    publish_mqtt_message(
                        f"public/request_live_data/{user_id}", "Send live data")
                    return HttpResponse(status=200, content="Success")
        except Exception as e:
            return HttpResponse(status=400, content=e)
        # Return a default response even if the message doesn't match any conditions
        return HttpResponse(status=200, content="Default response")
    else:
        # if other method is used, return Method Not Allowed
        return HttpResponse(status=405, content="Method Not Allowed")


# @csrf_exempt
# def line_webhook(request):
#     """Webhook for Line messaging API."""
#     if request.method != "POST":
#         return HttpResponse(status=405, content="Method Not Allowed")

#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         event_type = data['events'][0]['type']
#         user_id = data['events'][0]['source']['userId']
#         message = data['events'][0]['message']['text']

#         if not check_user_id(user_id):
#             return HttpResponse(status=400, content="User not found")

#         if event_type == "message":
#             return handle_message_type(user_id, message)

#     except json.JSONDecodeError as e:
#         return HttpResponse(status=400, content=f"JSON Error: {str(e)}")
#     except Exception as e:
#         return HttpResponse(status=400, content=f"Unexpected Error: {str(e)}")

#     return HttpResponse(status=200, content="Unhandled event type")

# def handle_message_type(user_id, message):
#     """Handle specific message types."""
#     if message == 'UserId':
#         return handle_user_id_message(user_id)
#     elif message == 'Live Data':
#         return handle_live_data_request(user_id)
#     # Respond with 200 OK for unsupported message types
#     return HttpResponse(status=200, content="Message type not handled")

# def handle_user_id_message(user_id):
#     """Handle 'UserId' message type."""
#     LineWebhook.objects.create(user_id=user_id, event_type='message')
#     if config('DEPLOYMENT', cast=bool):
#         # Assuming get_user_id is properly defined to handle a request and user_id
#         return get_user_id(RequestFactory().get(reverse('webhook_manager:get_user_id', kwargs={'user_id': user_id})), user_id)
#     return get_user_id(HttpResponse(), user_id)

# def handle_live_data_request(user_id):
#     """Publish live data message to MQTT broker and return success."""
#     publish_mqtt_message(f"b6510545608/request_live_data/{user_id}", "Send live data")
#     return HttpResponse(status=200, content="Success")


def check_user_id(user_id):
    """ Check if the user id is valid """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANEL_ACCESS_TOKEN}"
    }
    url = f"https://api.line.me/v2/bot/profile/{user_id}"
    return requests.get(url, headers=headers).status_code == 200


def get_user_id(request, user_id: str):
    """ Get user id from the request body """
    if request.method == "GET":
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CHANEL_ACCESS_TOKEN}"
        }
        payload = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": user_id
                }
            ]
        }
        response = requests.post(
            url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return HttpResponse(status=200, content="Success")
        return HttpResponse(status=400, content="Failed")
    return HttpResponse(status=405, content="Method Not Allowed")


def send_line_image(user_id: str, original_img_url: str, resize_img_url: str):
    """ Send image to the user """
    url = "https://api.line.me/v2/bot/message/push"
    payload = {
        "to": user_id,
        "messages":
            [
                {"type": "image",
                 "originalContentUrl": original_img_url,
                 "previewImageUrl": resize_img_url
                 }
            ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANEL_ACCESS_TOKEN}"
    }
    if check_user_id(user_id):
        response = requests.post(
            url, headers=headers, data=json.dumps(payload))
        return response
    return HttpResponse(status=400, content="User not found")


def publish_mqtt_message(topic, message):
    """ Publish a message to the MQTT broker """
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.username_pw_set(config('MQTT_USER'), config('MQTT_PASS'))
    mqtt_client.connect(config('MQTT_BROKER'),
                        config('MQTT_PORT', cast=int), 60)
    mqtt_client.publish(topic, message)
    mqtt_client.disconnect()
    return HttpResponse(status=200, content="Success")


def send_line_message(user_id, message):
    """ Send a message to the user"""
    url = "https://api.line.me/v2/bot/message/push"
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANEL_ACCESS_TOKEN}"
    }
    if check_user_id(user_id):
        response = requests.post(
            url, headers=headers, data=json.dumps(payload))
        return response
    return HttpResponse(status=400, content="User not found")
