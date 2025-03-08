# app/utils/image_processing.py
import os
import skimage.io
import torch
import torchvision
import torchxrayvision as xrv
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath

def process_image(image_path):
    # Read and preprocess image
    img = skimage.io.imread(image_path)
    
    # Handle grayscale images
    if len(img.shape) == 2:
        img = img[..., None]
    if len(img.shape) == 3 and img.shape[2] > 1:
        img = img.mean(2)
    
    # Normalize and prepare image
    img = xrv.datasets.normalize(img, 255)
    img = img[None, ...]  # Add channel dimension
    
    # Transform image
    transform = torchvision.transforms.Compose([
        xrv.datasets.XRayCenterCrop(),
        xrv.datasets.XRayResizer(224)
    ])
    
    img = transform(img)
    img = torch.from_numpy(img)
    
    return img