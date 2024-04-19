import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from prediction.predict import sensor_prediction, image_prediction
import base64
from PIL import Image
import io
import pickle


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
        
        # process image prediction
        prediction_result = image_prediction(img)
        # serialize the result so that it can return with HttpResponse
        serialized_result = pickle.dumps(prediction_result)
        
        return HttpResponse(serialized_result, content_type='application/octet-stream', status=200)
    
    return HttpResponse(status=405, content="Method Not Allowed")
