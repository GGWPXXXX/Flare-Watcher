from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import json
import requests
import os
from decouple import config
from .models import LineWebhook


@csrf_exempt
def line_webhook(request):
    if request.method == "POST":
        try:
            # create json object from the request body
            data = json.loads(request.body.decode("utf-8"))
            event_type = data['events'][0]['type']
            if event_type == "message":
                user_id = data['events'][0]['source']['userId']
                message = data['events'][0]['message']['text']
                #reply_token = data['events'][0]['replyToken']
                print(user_id, message)
                if user_id and message == 'UserId':
                    LineWebhook.objects.create(
                        user_id=user_id,
                        event_type=event_type,
                        #reply_token=reply_token
                    )
                    return redirect('get_user_id', user_id=user_id) #reply_token=reply_token)

                return HttpResponse(status=400, content="userId or message is missing")

            # handle other event types here
            return HttpResponse(status=200)
        except json.JSONDecodeError as e:
            # if JSON decoding error occurs
            return HttpResponse(status=400, content=str(e))
        except KeyError as e:
            # if necessary keys are not found in the data
            return HttpResponse(status=400, content="Key error: {}".format(str(e)))
    # handle non-POST requests
    return HttpResponse(status=405, content="Method Not Allowed")


def get_user_id(request, user_id):
    print("I'm here")
    if request.method == "GET":
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('CHANEL_ACCESS_TOKEN')}"
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
        print(config('CHANEL_ACCESS_TOKEN'))
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.status_code, response.text)
        if response.status_code == 200:
            return HttpResponse(status=200, content="Success")
        return HttpResponse(status=400, content="Failed")


@csrf_exempt
def test_post(request):
    if request.method == "POST":
        greeting = request.POST.get("greeting", "")
        LineWebhook.objects.create(event_type="test", user_id=greeting)
        return HttpResponse(status=200, content="Success")
    else:
        return HttpResponse(status=405, content="Method not allowed")
