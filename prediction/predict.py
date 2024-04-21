import numpy as np
from ultralytics import YOLO
import os
import requests
import pandas as pd
import pickle
import shutil
from PIL import Image, ImageDraw
import io
from django.core.files.base import ContentFile
from time import sleep

yolo_model_path = "prediction/model/yolo_object_detection.pt"
yolo_model_url = "https://media.githubusercontent.com/media/GGWPXXXX/Flare-Watcher/main/best.pt"


def set_up():
    """ Check to see whether the model file exists locally, if not download it from the url """
    # check if the model file exists locally
    if not os.path.exists(yolo_model_path):
        print("Downloading model file...")
        response = requests.get(yolo_model_url)
        with open(yolo_model_path, 'wb') as f:
            f.write(response.content)


def image_prediction(picture_url, picture_name):
    """ Predict the image using YOLO model to detect fire"""
    set_up()  # Assuming this function sets up the yolo_model_path
    model = YOLO(yolo_model_path)

    # Perform prediction
    model(picture_url, save=True, project="img", name=picture_name)
    return


def load_random_forest_model() -> object:
    """ Load the random forest model """
    with open('prediction/model/random_forest_model.pkl', 'rb') as f:
        clf2 = pickle.load(f)
    return clf2


def sensor_prediction(sensor_data: list) -> int:
    """ Predict whether the sensor data indicates a fire or not"""
    feature_names = ['Humidity[%]', 'TVOC[ppb]', 'eCO2[ppm]',
                     'Pressure[hPa]']
    return load_random_forest_model().predict(pd.DataFrame(np.array(sensor_data).reshape(1, -1), columns=feature_names))[0]


def central_system(data: dict):
    from . import models
    import json

    # Extract sensor data from the received data dictionary
    sensor_data = [
        data["Humidity[%]"],
        data["TVOC[ppb]"],
        data["eCO2[ppm]"],
        data["Pressure[hPa]"]
    ]

    # Predict using sensor data
    sensor_prediction_result = sensor_prediction(sensor_data)

    # Extract and remove the image from data
    before_predict_img = data.pop("img")

    # Convert the image to bytes
    image_bytes = io.BytesIO()
    before_predict_img.save(image_bytes, format='JPEG')
    image_data = image_bytes.getvalue()
    content_file = ContentFile(image_data)
    # create temp image to store in aws s3
    before_prediction_image = models.BeforePredictionImage()
    before_prediction_image.before_predict.save(
        'original_image.jpg', content_file)
    before_prediction_image.save()

    print("Created BeforePredictionImage object successfully!")
    # get url of the image
    url_img_before_predict = before_prediction_image.before_predict.url
    picture_name = url_img_before_predict.split('/')[-1]
    print(picture_name)
    print("url_img_before_predict: ", url_img_before_predict)
    

    image_prediction(url_img_before_predict, picture_name)
    
    with open(f"img/{picture_name}/{picture_name}", 'rb') as f:
        predicted_image_data = f.read()
    after_predicted_content = ContentFile(predicted_image_data)
    after_prediction_image = models.AfterPredictionImage()
    after_prediction_image.after_predict.save(
        'predicted_image.jpg', after_predicted_content)
    print("Created AfterPredictionImage object successfully!")
    url_img_after_predict = after_prediction_image.after_predict.url
    print("url_img_after_predict: ", url_img_after_predict)
    
    if os.path.exists(picture_name):
        os.remove(picture_name)
    else:
        print("The file does not exist")
    if os.path.exists(f"img/{picture_name}"):
        shutil.rmtree(f"img/{picture_name}")
    else:
        print("The directory does not exist")
    # print("Predicted image successfully!")

    # Print results
    print(sensor_prediction_result)
    # print(url_img_before_predict, url_img_after_predict)
