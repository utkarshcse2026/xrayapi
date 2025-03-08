# app/api/routes.py
from flask import Blueprint, request, jsonify
from app.models.predictor import XRayPredictor
from app.utils.image_processing import save_uploaded_file, allowed_file
import os

api_bp = Blueprint('api', __name__)
predictor = XRayPredictor()

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if image file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save and process the file
        filepath = save_uploaded_file(file)
        
        try:
            # Get predictions
            predictions = predictor.predict(filepath)
            
            # Clean up
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'predictions': predictions
            })
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Error processing image: {str(e)}'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500