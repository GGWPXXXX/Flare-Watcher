import torch
import os
import requests

model_path = "best.pt"
model_url = "https://media.githubusercontent.com/media/GGWPXXXX/Flare-Watcher/main/best.pt"

def set_up():
    # check if the model file exists locally
    if not os.path.exists(model_path):
        print("Downloading model file...")
        response = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(response.content)

def image_prediction(image_path):
    set_up()
    model = torch.load(model_path)
