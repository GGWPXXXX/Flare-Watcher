import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from prediction.predict import sensor_prediction, image_prediction
import base64


@csrf_exempt
def sensor_prediction_view(request):
    if request.method == "POST":
        # extract json object and pass it to the prediction function
        result = sensor_prediction(
            [i for i in json.loads(request.body.decode("utf-8")).values()])
        return HttpResponse(status=200, content=result)
    return HttpResponse(status=405, content="Method Not Allowed")

@csrf_exempt
def image_prediction_view(request):
    if request.method == "POST":
        # decode image from base 64 
        img = base64.b64decode(request.body.decode("utf-8"))
        print(image_prediction(img))
        return HttpResponse(status=200, content="Image prediction completed")
    return HttpResponse(status=405, content="Method Not Allowed")
