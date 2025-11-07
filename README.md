# IMDb Rating Classification API

**API REST para predicción de categoría de rating de películas**

Proyecto MLOps - Grupo 21

## 📋 Descripción

API REST desarrollada con FastAPI que permite predecir la categoría de rating de películas de IMDb (Poor, Average, Good, Excellent) basándose en sus características.

## 🚀 Características

- **FastAPI**: Framework moderno y rápido para APIs
- **Validación automática**: Pydantic models para validación de entrada/salida
- **Documentación interactiva**: Swagger UI y ReDoc generados automáticamente
- **Modelo ML integrado**: Carga automática del modelo entrenado
- **Endpoints RESTful**: Diseño limpio y estándar

## 🏗️ Arquitectura

```
.
├── main.py              # Aplicación FastAPI principal
├── requirements.txt     # Dependencias Python
└── .venv/              # Entorno virtual (local)
```

## 📡 Endpoints

### `GET /`
Información general de la API

**Respuesta:**
```json
{
  "message": "IMDb Rating Classification API",
  "version": "1.0.0",
  "endpoints": {
    "/health": "Health check",
    "/predict": "Predict rating category",
    "/model-info": "Model information"
  }
}
```

### `GET /health`
Verificar el estado de la API y del modelo

**Respuesta:**
```json
{
  "status": "healthy",
  "model_path": "/path/to/model.pkl",
  "model_exists": true,
  "metadata_exists": true
}
```

### `GET /model-info`
Obtener información del modelo cargado

**Respuesta:**
```json
{
  "model_name": "logistic_regression",
  "metrics": {
    "accuracy": 0.9999,
    "f1_score_weighted": 0.9999
  },
  "parameters": {...}
}
```

### `POST /predict`
Predecir categoría de rating para películas

**Request Body:**
```json
{
  "movies": [
    {
      "startYear": 2020.0,
      "runtimeMinutes": 120.0,
      "numVotes": 1000.0,
      "averageRating": 7.5,
      "runtime_category": "Standard (90-120m)",
      "popularity": "Low"
    }
  ]
}
```

**Respuesta:**
```json
{
  "predictions": [
    {
      "rating_category": "Good",
      "confidence": 0.9876
    }
  ],
  "model_name": "logistic_regression",
  "model_metrics": {
    "accuracy": 0.9999,
    "f1_score_weighted": 0.9999
  }
}
```

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.12+
- Modelo entrenado en `../sentiment_classification_model/models/best_model.pkl`

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/api_imdb.git
cd api_imdb
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Ejecutar la API
```bash
# Modo desarrollo (con hot-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Modo producción
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Acceder a la documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Configuración

### Variables de Entorno

```bash
# Ruta al modelo entrenado (opcional)
export MODEL_PATH=/path/to/custom/model.pkl

# Ruta a metadata del modelo (opcional)
export METADATA_PATH=/path/to/custom/metadata.json
```

### Valores por Defecto

Si no se especifican las variables de entorno, la API busca el modelo en:
- `../sentiment_classification_model/models/best_model.pkl`
- `../sentiment_classification_model/models/best_model_metadata.json`

## 🧪 Pruebas

### Usando cURL

```bash
# Health check
curl http://localhost:8000/health

# Predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "movies": [{
      "startYear": 2020.0,
      "runtimeMinutes": 120.0,
      "numVotes": 1000.0,
      "averageRating": 7.5,
      "runtime_category": "Standard (90-120m)",
      "popularity": "Low"
    }]
  }'
```

### Usando Python

```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "movies": [{
        "startYear": 2020.0,
        "runtimeMinutes": 120.0,
        "numVotes": 1000.0,
        "averageRating": 7.5,
        "runtime_category": "Standard (90-120m)",
        "popularity": "Low"
    }]
}

response = requests.post(url, json=payload)
print(response.json())
```

## 📦 Dependencias Principales

- `fastapi==0.115.0` - Framework web
- `uvicorn==0.30.3` - Servidor ASGI
- `scikit-learn==1.5.2` - ML para cargar modelos
- `pandas==2.2.2` - Manipulación de datos
- `pydantic==2.8.2` - Validación de datos

## 🐳 Docker (Opcional)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build
docker build -t imdb-rating-api .

# Run
docker run -p 8000:8000 imdb-rating-api
```

## 👥 Equipo - Grupo 21

- **Luis Felipe González** - Data Manager/MLOps
- **Daniel Ricardo Marín** - Data Scientist
- **Manuel Alejandro Bayona** - Cloud Engineer
- **Fabián Jiménez** - BI Analyst

## 📄 Licencia

Este proyecto es parte del curso de MLOps - MIAD Universidad de los Andes.

## 🔗 Repositorios Relacionados

- [Modelo y Pipeline](https://github.com/mbayonal/sentiment_classification_model) - Entrenamiento y DVC
- [Dashboard](https://github.com/mbayonal/dashboard_imdb) - Interfaz web con Streamlit
