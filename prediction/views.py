import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from prediction.predict import sensor_prediction, image_prediction
import base64
from PIL import Image
import matplotlib.pyplot as plt
import io
import pickle


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
        image_data = request.body.decode("utf-8")
        # if your image is jpeg
        image_data = image_data.replace("data:image/jpeg;base64,", "")  
        # if your image is png
        image_data = image_data.replace("data:image/png;base64,", "")  
        # Open image with PIL
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        
        # Process image prediction
        prediction_result = image_prediction(img)
        for i in prediction_result:
            i.show()
        serialized_result = pickle.dumps(prediction_result)
        
        return HttpResponse(status=200, content="Image prediction completed", data=prediction_result)
    
    return HttpResponse(status=405, content="Method Not Allowed")
