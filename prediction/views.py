import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from prediction.predict import sensor_prediction

@csrf_exempt
def sensor_prediction_view(request):
    if request.method == "POST":
        # extract json object and pass it to the prediction function
        result = sensor_prediction([i for i in json.loads(request.body.decode("utf-8")).values()])
        return HttpResponse(status=200, content=json.dumps({"prediction": result}))
    return HttpResponse(status=405, content="Method Not Allowed") 
    
