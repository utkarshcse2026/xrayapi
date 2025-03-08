# Procfile
web: gunicorn wsgi:app --workers=4 --threads=2 --timeout 120 --bind 0.0.0.0:$PORT

# render.yaml
services:
  - type: web
    name: xray-prediction-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn wsgi:app --workers=4 --threads=2 --timeout 120 --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: FLASK_ENV
        value: production
    healthCheckPath: /health
    autoDeploy: true