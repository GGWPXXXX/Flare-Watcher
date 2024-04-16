from ultralytics import YOLO
import os
import requests

yolo_model_path = "../Flare-Watcher/prediction/model/yolo_object_detection.pt"
yolo_model_url = "https://media.githubusercontent.com/media/GGWPXXXX/Flare-Watcher/main/best.pt"


def set_up():
    # check if the model file exists locally
    if not os.path.exists(yolo_model_path):
        print("Downloading model file...")
        response = requests.get(yolo_model_url)
        with open(yolo_model_path, 'wb') as f:
            f.write(response.content)


def image_prediction(image_path):
    set_up()
    # load and predict
    model = YOLO('best.pt')
    results = model(image_path)
    for i in results:
        i.show()
        