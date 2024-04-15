import torch
import os
import requests

model_path = "best.pt"
print(os.path.exists(model_path))
# check if the model file exists locally
if not os.path.exists(model_path):
    model_url = "https://raw.githubusercontent.com/GGWPXXXX/Flare-Watcher/main/best.pt"
    response = requests.get(model_url)
    with open(model_path, 'wb') as f:
        f.write(response.content)

model = torch.load(model_path)
