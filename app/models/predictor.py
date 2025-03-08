# app/models/predictor.py
import torchxrayvision as xrv
import torch
from app.utils.image_processing import process_image

class XRayPredictor:
    def __init__(self):
        self.model = xrv.models.DenseNet(weights="densenet121-res224-all")
        self.model.eval()
    
    def predict(self, image_path):
        # Process image
        img = process_image(image_path)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(img[None, ...])
        
        # Convert predictions to dictionary
        predictions = dict(zip(self.model.pathologies, outputs[0].numpy().tolist()))
        
        return predictions