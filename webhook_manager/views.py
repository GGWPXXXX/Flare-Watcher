from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
from decouple import config
from .models import LineWebhook


@csrf_exempt
def line_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        event_type = data['events'][0]['type']
        user_id = data['events'][0]['source']['userId']

        # save data to database
        LineWebhook.objects.create(event_type=event_type, user_id=user_id)

        # return success response
        return HttpResponse(status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})


def test_env(request):
    node_red_url = config("MSG_TEST")
    return JsonResponse({"node_red_url": node_red_url})


def get_line_user_id(request):
    if request.method == "GET":
        last_record = LineWebhook.objects.last()

        if last_record:
            return JsonResponse({"last_user_id": last_record.user_id})
        else:
            return HttpResponse(status=404, content="No record found")
    # if any other request method is used
    return HttpResponse(status=400, content="Invalid request method")
