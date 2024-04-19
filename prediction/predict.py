import numpy as np
from ultralytics import YOLO
import os
import requests
import pandas as pd
import pickle

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


def image_prediction(image_path) -> dict:
    """ Predict the image using YOLO model to detect fire"""
    set_up()
    # load and predict
    model = YOLO(yolo_model_path)
    return model(image_path)


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
