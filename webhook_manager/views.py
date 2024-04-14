from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
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
            if event_type == "follow":
                user_id = data['events'][0]['source']['userId']
                if user_id:
                    LineWebhook.objects.create(
                        user_id=user_id,
                        event_type=event_type
                    )
                    return HttpResponse(status=200)
                return HttpResponse(status=400, content="userId is missing")
            elif event_type == "message":
                user_id = data['events'][0]['source']['userId']
                message = data['events'][0]['message']['text']
                print(user_id, message)
                if user_id and message:
                    LineWebhook.objects.create(
                        user_id=user_id,
                        event_type=event_type,
                        reply_token=data['events'][0]['replyToken']
                    )
                    return HttpResponse(status=200)
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


def get_last_user_id(request):
    if request.method == "GET":
        last_record = LineWebhook.objects.last()
        if last_record:
            return JsonResponse({"user_id": last_record.user_id, "reply_token": last_record.reply_token if last_record.reply_token else ""})
        else:
            return HttpResponse(status=404, content="No record found")
    # if any other request method is used
    return HttpResponse(status=400, content="Invalid request method")


@csrf_exempt
def test_post(request):
    if request.method == "POST":
        greeting = request.POST.get("greeting", "")
        LineWebhook.objects.create(event_type="test", user_id=greeting)
        return HttpResponse(status=200, content="Success")
    else:
        return HttpResponse(status=405, content="Method not allowed")
