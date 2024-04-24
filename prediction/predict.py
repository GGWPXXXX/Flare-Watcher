import numpy as np
from ultralytics import YOLO
import os
import pandas as pd
import pickle
import shutil
import io
from django.core.files.base import ContentFile
from time import sleep
from PIL import Image
from .const import WARNING_MSG, ALERT_MSG

yolo_model_path = "prediction/model/yolo_object_detection.pt"


def set_up():
    """ Check to see whether the model file exists locally, if not download it from the url """
    # check if the model file exists locally
    if not os.path.exists(yolo_model_path):
        return Exception("Model file does not exist")


def image_prediction(picture_url, picture_name):
    """ Predict the image using YOLO model to detect fire"""
    set_up()  # Assuming this function sets up the yolo_model_path
    model = YOLO(yolo_model_path)

    # Perform prediction
    return model(picture_url, save=True, project="img", name=picture_name)


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
    from webhook_manager import views

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
    before_predict_img.save(image_bytes, format='JPEG', optimize=True)
    image_data = image_bytes.getvalue()

    content_file = ContentFile(image_data)
    # create temp image to store in aws s3
    before_prediction_image = models.BeforePredictionImage()
    before_prediction_image.before_predict.save(
        'original_image.jpg', content_file)
    before_prediction_image.save()

    print("Created PreviewPredictionImage object successfully!")
    # get url of the image
    url_img_before_predict = before_prediction_image.before_predict.url
    picture_name = url_img_before_predict.split('/')[-1]
    print(picture_name)
    print("url_preview_img_predict: ", url_img_before_predict)

    image_pred_results = image_prediction(url_img_before_predict, picture_name)

    with open(f"img/{picture_name}/{picture_name}", 'rb') as f:
        predicted_image_data = f.read()

    # after predict image in original size
    original_after_predict_content = ContentFile(predicted_image_data)
    original_after_predict_image = models.OriginalSizePredictionImage()
    original_after_predict_image.after_predict.save(
        'original_predicted_image.jpg', original_after_predict_content)
    url_original_img_after_predict = original_after_predict_image.after_predict.url
    print("url_original_img_after_predict: ", url_original_img_after_predict)

    resized_picture = resize_and_compress_image(predicted_image_data)
    resize_after_predicted_content = ContentFile(resized_picture)
    resize_after_prediction_image = models.CompressedPredictionImage()
    resize_after_prediction_image.after_predict.save(
        'resized_predicted_image.jpg', resize_after_predicted_content)
    print("Created AfterPredictionImage object successfully!")
    url_resize_img_after_predict = resize_after_prediction_image.after_predict.url
    print("url_resize_img_after_predict: ", url_resize_img_after_predict)

    if os.path.exists(picture_name):
        os.remove(picture_name)
    else:
        print("The file does not exist")
    if os.path.exists(f"img/{picture_name}"):
        shutil.rmtree(f"img/{picture_name}")
    else:
        print("The directory does not exist")
    print(sensor_prediction_result)

    # check if there is any fire detected in the image
    pred_result = 0
    for i in image_pred_results:
        if len(i.boxes.xyxy) != 0:
            pred_result = 1
            break
    indicator = int(data["flame_sensor"]) + sensor_prediction_result + pred_result
    print(f"Indicator score: {indicator}")
    # if at least 2 out of 3 sources indicate fire send warning message
    if indicator == 2:
        formatted_msg = WARNING_MSG.format("✅" if sensor_prediction_result == 1 else "❌",
                                           "✅" if pred_result == 1 else "❌", "✅" if data["flame_sensor"] == 1 else "❌")
        # send line message
        msg_result = views.send_line_message(data["user_id"], formatted_msg)
        print(f"Send messgae with response: {msg_result}")
        # send line image
        result = views.send_line_image(
            data["user_id"], url_original_img_after_predict, url_resize_img_after_predict)
        print(f"Send image with response: {result}")
    # if all 3 sources indicate fire send alert message
    elif indicator == 3:
        formatted_msg = ALERT_MSG.format("✅" if sensor_prediction_result == 1 else "❌",
                                         "✅" if pred_result == 1 else "❌", "✅" if data["flame_sensor"] == 1 else "❌")
        # send line message
        msg_result = views.send_line_message(data["user_id"], formatted_msg)
        print(f"Send messgae with response: {msg_result}")
        # send line image
        img_result = views.send_line_image(
            data["user_id"], url_original_img_after_predict, url_resize_img_after_predict)
        print(f"Send image with response: {img_result}")
    else:
        print("No fire detected")


def resize_and_compress_image(image_data, max_size=1024, max_file_size=1024 * 1024):
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail((max_size, max_size), Image.LANCZOS)

    resized_image_bytes = io.BytesIO()
    quality = 90
    while True:
        img.save(resized_image_bytes, format='JPEG',
                 optimize=True, quality=quality)
        resized_image_data = resized_image_bytes.getvalue()
        if len(resized_image_data) <= max_file_size:
            break
        quality -= 10
        resized_image_bytes = io.BytesIO()
        if quality < 10:
            print("Unable to reduce image size below the specified limit.")
            break

    return resized_image_data
