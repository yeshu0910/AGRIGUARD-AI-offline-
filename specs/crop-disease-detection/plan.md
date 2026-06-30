# Implementation Plan: Crop Disease Detection

## Architecture

The detection pipeline consists of:
1. Image upload endpoint (`/detect`) in `app.py`
2. Preprocessing in `preprocess.py` (resize, normalize)
3. Model inference in `detect.py` using TFLite
4. Label parsing in `crop_detector.py`
5. Recommendation generation in `recommendation.py` and `llm.py`

## Components

| Component | File | Responsibility |
|-----------|------|----------------|
| API Layer | `app.py` | FastAPI endpoints |
| Preprocessing | `preprocess.py` | Image loading and transformation |
| Detection | `detect.py` | TFLite model wrapper |
| Label Parser | `crop_detector.py` | Parse PlantVillage labels |
| Database | `database.py` | SQLite storage |
| Recommendation | `recommendation.py` | Curated treatment knowledge |
| LLM Client | `llm.py` | Local LLM integration |

## Data Flow

```
Image Upload -> preprocess() -> predict() -> parse_label() -> get_recommendation() -> JSON Response
```

## Dependencies

- TFLite model for inference (../models/plant_disease.tflite)
- SQLite database (../database/history.db)