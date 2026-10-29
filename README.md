# AeroScope

AeroScope is an air-quality analysis dashboard with a Java Spring Boot web layer, HTML/CSS/JavaScript frontend, and a Python FastAPI machine-learning service.

## Requirements
- Java 21
- Maven 3.9+
- Python 3.10+

## Run the Python ML service
```bash
cd python-ml
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Run the Java web app
In a second terminal:
```bash
cd java-web
mvn spring-boot:run
```
Open http://localhost:8080.

The Java service proxies requests to Python at http://localhost:8000. Set `ML_SERVICE_URL` to change that address.

## ML notes
Pattern analysis uses K-Means, PCA, and silhouette score. The forecast endpoint is a simple baseline trend model for experimentation, not a validated air-quality forecast. Use quality-checked historical data and evaluate the model before relying on predictions.