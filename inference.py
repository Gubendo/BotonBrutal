from torchvision import models
from utils import transform_image

model = models.densenet121(pretrained=True)
model.eval()

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    return str(y_hat.item())

