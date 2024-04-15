from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
import requests
from decouple import config
from .models import LineWebhook
from django.test.client import RequestFactory


@csrf_exempt
def line_webhook(request):
    factory = RequestFactory()
    if request.method == "POST":
        try:
            # create json object from the request body
            data = json.loads(request.body.decode("utf-8"))
            event_type = data['events'][0]['type']
            if event_type == "message":
                user_id = data['events'][0]['source']['userId']
                message = data['events'][0]['message']['text']
                if user_id and message == 'UserId':
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
        except Exception as e:
            return HttpResponse(status=400, content="Error processing webhook")
    # if other method is used, return Method Not Allowed
    return HttpResponse(status=405, content="Method Not Allowed")


def get_user_id(request, user_id):
    if request.method == "GET":
        chanel_access_token = config('CHANEL_ACCESS_TOKEN')
        if chanel_access_token:
            url = "https://api.line.me/v2/bot/message/push"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {chanel_access_token}"
            }
            data = {
                "to": user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": user_id
                    }
                ]
            }
            response = requests.post(
                url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return HttpResponse(status=200, content="Success")
            return HttpResponse(status=400, content="Failed")
        return HttpResponse(status=400, content="CHANEL_ACCESS_TOKEN not found in environment")
    return HttpResponse(status=405, content="Method Not Allowed")
