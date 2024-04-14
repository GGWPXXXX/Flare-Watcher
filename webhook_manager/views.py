from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decouple import config
from .models import LineWebhook


@csrf_exempt
def line_webhook(request):
    if request.method == "POST":
        # data = json.loads(request.body.decode("utf-8"))
        # event_type = data['events'][0]['type']
        # user_id = data['events'][0]['source']['userId']

        # save data to database
        # LineWebhook.objects.create(event_type=event_type, user_id=user_id)

        # return success response
        return HttpResponse(status=200)
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
        if request.content_type == "multipart/form-data":
            greeting = request.POST.get("greeting", "")
            LineWebhook.objects.create(event_type="test", user_id=greeting)
            return HttpResponse(status=200, content="Success")
        else:
            # Handle other content types or empty body
            if not request.body:
                return HttpResponseBadRequest("Empty request body")
            # You can handle different content types or formats as needed
            return HttpResponseBadRequest("Invalid content type")
    else:
        return HttpResponse(status=405, content="Method not allowed")
