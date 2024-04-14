from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decouple import config
from .models import LineWebhook


import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Assuming LineWebhook is your Django model for storing webhook data
from .models import LineWebhook


@csrf_exempt
def line_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_id = data['source']['userId']
            LineWebhook.objects.create(user_id=user_id)

            # Return success response
            return HttpResponse(status=200)
        except KeyError:
            # if the required key is not present in the JSON data
            return HttpResponse(status=400, content="Invalid JSON data")
        except json.JSONDecodeError:
            # uf the request body is not valid JSON
            return HttpResponse(status=400, content="Invalid JSON format")
    else:
        return HttpResponse(status=405, content="Method not allowed")


def get_line_user_id(request):
    if request.method == "GET":
        last_record = LineWebhook.objects.last()

        if last_record:
            return JsonResponse({"last_user_id": last_record.user_id})
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
