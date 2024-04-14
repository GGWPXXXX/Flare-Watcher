from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decouple import config
from .models import LineWebhook


@csrf_exempt
def line_webhook(request):
    if request.method == "POST":
        try:
            # create json object from the request body
            data = json.loads(request.body.decode("utf-8"))

            event_type = data['events'][0]['type']
            user_id = data['events'][0]['source']['userId']

            if user_id:
                LineWebhook.objects.create(
                    user_id=user_id, event_type=event_type)
                return HttpResponse(status=200)
            else:
                # if userId is missing from the data
                return HttpResponse(status=400, content="userId is missing")

        except json.JSONDecodeError as e:
            # if JSON decoding error occurs
            return HttpResponse(status=400, content=str(e))

        except KeyError as e:
            # if necessary keys are not found in the data
            return HttpResponse(status=400, content="Key error: {}".format(str(e)))

        except Exception as e:
            # If any other error occurs
            return HttpResponse(status=400, content=str(e))

    else:
        return HttpResponse(status=405, content="Method not allowed")


def get_last_user_id(request):
    if request.method == "GET":
        last_record = LineWebhook.objects.last()
        print(last_record)
        if last_record:
            return JsonResponse({"last_user_id": last_record.user_id})
        else:
            return HttpResponse(status=404, content="No record found")
    # if any other request method is used
    return HttpResponse(status=400, content="Invalid request method")
