#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IMDb Rating Category Classification API

Predicts rating category (Poor, Average, Good, Excellent) for movies
based on their features: decade, runtime, genres, popularity, etc.
"""

import os
import json
from pathlib import Path
from typing import List, Optional

import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
DEFAULT_MODEL_PATH = ROOT_DIR / "sentiment_classification_model" / "models" / "best_model.pkl"
DEFAULT_METADATA_PATH = ROOT_DIR / "sentiment_classification_model" / "models" / "best_model_metadata.json"

MODEL_PATH = Path(os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH)))
METADATA_PATH = Path(os.getenv("METADATA_PATH", str(DEFAULT_METADATA_PATH)))

app = FastAPI(
    title="IMDb Rating Classification API",
    description="Predict movie rating category from features",
    version="1.0.0"
)


class MovieFeatures(BaseModel):
    """Features for a single movie"""
    startYear: float = Field(..., description="Release year")
    runtimeMinutes: float = Field(..., description="Runtime in minutes")
    numVotes: float = Field(..., description="Number of votes")
    averageRating: float = Field(..., description="Average rating (1-10)")
    runtime_category: str = Field(..., description="Runtime category")
    popularity: str = Field(..., description="Popularity category")


class PredictRequest(BaseModel):
    movies: List[MovieFeatures] = Field(..., description="List of movies to classify")


class PredictionResult(BaseModel):
    rating_category: str
    confidence: Optional[float] = None


class PredictResponse(BaseModel):
    predictions: List[PredictionResult]
    model_name: str
    model_metrics: dict


_model = None
_metadata = None


def load_model():
    global _model, _metadata
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    
    if _metadata is None and METADATA_PATH.exists():
        with open(METADATA_PATH, 'r') as f:
            _metadata = json.load(f)
    
    return _model, _metadata


@app.get("/")
async def root():
    return {
        "message": "IMDb Rating Classification API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/predict": "Predict rating category",
            "/model-info": "Model information"
        }
    }


@app.get("/health")
async def health():
    try:
        model_exists = MODEL_PATH.exists()
        metadata_exists = METADATA_PATH.exists()
        return {
            "status": "healthy" if model_exists else "model_missing",
            "model_path": str(MODEL_PATH),
            "model_exists": model_exists,
            "metadata_exists": metadata_exists
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.get("/model-info")
async def model_info():
    try:
        _, metadata = load_model()
        if metadata:
            return metadata
        return {"message": "No metadata available"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest):
    """Predict rating category for movies"""
    try:
        model, metadata = load_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {e}")

    if not payload.movies:
        raise HTTPException(status_code=400, detail="'movies' list cannot be empty")

    try:
        # Convert input to DataFrame
        movies_data = [movie.model_dump() for movie in payload.movies]
        X = pd.DataFrame(movies_data)
        
        # Predict
        predictions = model.predict(X)
        
        # Get probabilities if available
        probs = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            # Get max probability for each prediction
            probs = proba.max(axis=1).tolist()
        
        # Build response
        results = []
        for i, pred in enumerate(predictions):
            result = PredictionResult(
                rating_category=pred,
                confidence=probs[i] if probs else None
            )
            results.append(result)
        
        model_name = metadata.get('model_name', 'unknown') if metadata else 'unknown'
        model_metrics = metadata.get('metrics', {}) if metadata else {}
        
        return PredictResponse(
            predictions=results,
            model_name=model_name,
            model_metrics=model_metrics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")


# To run locally: uvicorn main:app --reload --host 0.0.0.0 --port 8000
