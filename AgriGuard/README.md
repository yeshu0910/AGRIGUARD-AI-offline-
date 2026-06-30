# AgriGuard AI

**Offline crop disease detection for farmers.**
Runs entirely on CPU, requires no internet connection, and stores all data locally.

## Requirements

- Python 3.11+
- No GPU needed (CPU-only inference)
- ~2 GB free disk space (models)

## Installation

```bash
# 1. Install Python dependencies
pip install -r backend/requirements.txt
```

## Model Setup

1. **Download `disease_model.tflite`** (PlantVillage-trained, 57 classes):
   - A pre-converted TFLite model is provided in `models/` directory
   - Or convert from the sibling project's H5 model

2. **Download `phi3.gguf`** (Phi-3 Mini GGUF for local LLM):
   - From: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf
   - Place at: `models/phi3.gguf`

> If the LLM model is missing, AgriGuard falls back to hardcoded disease-specific reports.
> If the TFLite model is missing, the `/detect` endpoint returns a 503 error with a helpful message.

## Run

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

Then open `frontend/index.html` in your browser (or serve it via any static server).

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/detect` | Upload leaf image for disease detection |
| GET | `/history` | List all detection logs (optional `?crop=` & `?severity=` filters) |
| GET | `/history/{id}` | Get single log entry by ID |
| DELETE | `/history/{id}` | Delete a log entry and its image |
| GET | `/export/csv` | Download all logs as CSV |
| GET | `/export/json` | Download all logs as JSON |
| GET | `/health` | Check model, DB, and disk status |

## Folder Structure

```
AgriGuard/
├── models/
│   ├── disease_model.tflite   # PlantVillage TFLite model
│   └── phi3.gguf              # Phi-3 Mini GGUF (local LLM)
├── database/
│   └── agriguard.db           # SQLite database (auto-created)
├── images/                    # Saved leaf images from scans
├── backend/
│   ├── app.py                 # FastAPI main entry point
│   ├── detect.py              # TFLite inference + OpenCV preprocessing
│   ├── llm.py                 # llama.cpp local LLM report generation
│   ├── database.py            # SQLite schema + CRUD operations
│   └── requirements.txt       # Python dependencies
├── frontend/
│   └── index.html             # Single-file HTML/JS/CSS frontend
├── assets/
└── README.md
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11, FastAPI, Uvicorn |
| AI Model | TensorFlow Lite (.tflite) |
| Image Proc | OpenCV (cv2) |
| Local LLM | llama-cpp-python (Phi-3 Mini GGUF) |
| Database | SQLite3, aiosqlite |
| Frontend | Vanilla HTML + CSS + JS (offline-safe) |
| Dataset | PlantVillage (57 classes) |

## PlantVillage Classes

Apple (scab, black rot, cedar rust, healthy), Banana (Panama disease, Black sigatoka, healthy), Chili (Leaf curl, Bacterial spot, healthy), Corn (Cercospora leaf spot, Common rust, Northern Leaf Blight, healthy), Cotton (Bacterial blight, Leaf curl, healthy), Grapes (Black rot, Esca, Leaf blight, healthy), Groundnut (Early leaf spot, Late leaf spot, healthy), Mango (Anthracnose, Powdery mildew, healthy), Potato (Early blight, Late blight, healthy), Rice (Brown spot, Leaf blast, Neck blast, healthy), Soybean (Bacterial blight, Frog eye leaf spot, healthy), Sugarcane (Red rot, Smut, healthy), Sunflower (Downy mildew, Leaf blast, healthy), Tomato (Bacterial spot, Early blight, Late blight, Leaf Mold, Septoria leaf spot, Spider mites, Target Spot, Yellow Leaf Curl Virus, Mosaic virus, healthy), Wheat (Brown rust, Yellow rust, Septoria, healthy).
