import torch
import os
import requests

# Local path to save the model
model_path = "your_model.pt"

# Check if the model file exists locally
if not os.path.exists(model_path):
    # Download the model from GitHub using the raw file URL
    model_url = "https://raw.githubusercontent.com/GGWPXXXX/Flare-Watcher/main/best.pt"
    response = requests.get(model_url)
    
    # Save the downloaded model to a local file
    with open(model_path, 'wb') as f:
        f.write(response.content)

# Load the model using PyTorch
model = torch.load(model_path)
