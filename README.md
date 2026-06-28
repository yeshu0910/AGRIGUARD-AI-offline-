# AgriGuard AI – Offline Crop Disease Logger

![Hackathon Phase](https://img.shields.io/badge/phase-1-blue)
![Status](https://img.shields.io/badge/status-phase_1-completed-green)
![Platform](https://img.shields.io/badge/platform-offline_only-red)

## Project Overview

**AgriGuard AI** is a fully offline, CPU-first artificial intelligence application designed to detect crop diseases from leaf images without any internet connection. Built for the **Offline Local AI Hackathon**, it empowers small and marginal farmers to diagnose plant health instantly using a smartphone or laptop, regardless of network availability.

The application combines a TensorFlow Lite classification model running on-device with a local small language model (Phi-3 Mini GGUF via llama.cpp) to generate structured, actionable treatment recommendations. All inference, storage, and reporting happen locally on CPU.

## Problem Statement

Over 500 million smallholder farmers worldwide lose 20–40% of crop yield annually to pests and diseases. Existing digital agri-advisory services require internet, smartphones with data plans, and cloud subscriptions — barriers that exclude the most vulnerable farming communities. Extension officers and farmers in rural areas often wait days for expert advice, by which time the disease has spread irreversibly.

There is an urgent need for an **offline, zero-cost, privacy-preserving** diagnostic tool that runs on commodity hardware.

## Solution

AgriGuard AI provides a complete offline AI pipeline:

1. **Ingest** – Farmer or extension officer captures a leaf photo via the offline web interface.
2. **Preprocess** – OpenCV normalizes the image (resize, color space, edges).
3. **Classify** – A quantized TensorFlow Lite model runs on CPU to identify the disease.
4. **Recommend** – A local LLM (Phi-3 Mini, 4-bit GGUF) generates structured JSON treatment steps.
5. **Store** – SQLite persists the diagnosis, confidence score, and recommendations locally.
6. **Report** – A responsive dashboard lists history, trends, and exportable reports.

No data leaves the device. No API keys, no cloud, no network required.

## Features

- 🚫 **100% Offline** – No internet, no cloud APIs, no OpenAI.
- ⚡ **CPU-Only Inference** – Optimized for Intel/AMD/ARM processors.
- 📱 **Responsive Web UI** – Works on phones, tablets, and desktops.
- 🧠 **Local LLM Recommendations** – Phi-3 Mini via llama.cpp gives structured advice.
- 📊 **SQLite History** – Full audit trail with timestamp, image path, and confidence.
- 📤 **JSON Export** – Machine-readable reports for integration or printing.
- 🔒 **Privacy First** – All data stays on-device.

## Architecture Diagram

```
Leaf Image
    ↓
OpenCV Preprocessing
    ↓
TensorFlow Lite Model
    ↓
Phi-3 Mini (llama.cpp)
    ↓
JSON Report
    ↓
SQLite Storage
    ↓
Responsive Dashboard
```

| Component | Role |
|---|---|
| Leaf Image | User-captured photo of affected crop |
| OpenCV | Resize, normalize, edge enhancement |
| TensorFlow Lite | On-device disease classification |
| Phi-3 Mini (llama.cpp) | Local LLM generates structured recommendations |
| JSON Report | Structured output with confidence & advice |
| SQLite | Persistent offline storage |
| Dashboard | Gallery, filters, history, export |

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5 + Tailwind CSS + Vanilla JS | Responsive offline PWA-capable UI |
| **Backend / API** | FastAPI (Python) | REST endpoints, CORS, async I/O |
| **Image Processing** | OpenCV (Python) | Resize, normalize, augment |
| **Inference Engine** | TensorFlow Lite (Python) | Quantized CPU-only classification |
| **LLM Runtime** | llama.cpp + Phi-3 Mini GGUF | 4-bit quantized local text generation |
| **Database** | SQLite3 + SQLAlchemy | Structured schema, full-text search |
| **Serialization** | Pydantic v2 | JSON schema validation, API contracts |
| **Packaging** | PyInstaller / Docker | Portable exe / container build |

## Folder Structure

```
AgriGuard_AI/
├── backend/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entrypoint
│   ├── config.py                    # env config, paths
│   ├── database/
│   │   ├── __init__.py
│   │   ├── engine.py                # SQLAlchemy engine + session factory
│   │   ├── models.py                # SQLAlchemy ORM
│   │   ├── schemas.py               # Pydantic DTOs
│   │   ├── crud.py                  # DB helpers
│   │   └── migrate.py               # Migration runner
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── disease.py               # /api/diagnose endpoint
│   │   ├── history.py               # /api/history endpoints
│   │   ├── stats.py                 # /api/stats endpoints
│   │   └── export.py                # /api/export endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── preprocessor.py          # OpenCV pipeline
│   │   ├── tflite_inference.py      # TF Lite model wrapper
│   │   ├── llm_service.py           # llama.cpp wrapper
│   │   └── report_builder.py        # JSON / PDF assembly
│   └── tests/
│       ├── __init__.py
│       ├── test_preprocessing.py
│       ├── test_inference.py
│       ├── test_llm.py
│       └── test_api.py
├── frontend/
│   ├── index.html
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── src/
│   │   ├── css/
│   │   │   └── main.css
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   ├── api.js
│   │   │   ├── camera.js
│   │   │   ├── gallery.js
│   │   │   └── dashboard.js
│   │   └── assets/
│   │       ├── icons/
│   │       └── images/
│   └── build/                       # Production bundle
├── models/
│   ├── crop_disease_model.tflite
│   ├── labels.txt
│   └── phi-3-mini-4k-instruct-q4.gguf
├── database/
│   ├── agriguard.db                 # SQLite runtime file (gitignored)
│   └── schema.sql                   # DDL for reference
├── images/
│   ├── sample_01.jpg
│   ├── sample_02.jpg
│   └── README_images.md             # Attribution / sources
├── assets/
│   ├── logo.svg
│   └── favicon.ico
├── docs/
│   ├── README.md
│   ├── SPECIFICATION_KIT.md
│   ├── GITLAB_ISSUES.md
│   ├── WORK_DIVISION_PLAN.md
│   ├── PROJECT_TIMELINE.md
│   ├── DELIVERABLES.md
│   ├── FOLDER_STRUCTURE.md
│   ├── ARCHITECTURE_DIAGRAM.md
│   ├── PROJECT_SCOPE.md
│   └── HACKATHON_ALIGNMENT.md
├── tests/
│   └── integration/                 # End-to-end pipeline tests
├── .gitignore
├── LICENSE                          # GNU AGPLv3 License
├── requirements.txt                 # Python deps
├── requirements-dev.txt             # Testing deps
└── pyproject.toml                   # Build system metadata
```

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend build)
- CMake 3.18+ (for llama.cpp build)
- Git

### Quick Start (Development)

```bash
# 1. Clone the repository
git clone <repository-url>
cd AgriGuard_AI

# 2. Set up Python environment
python -m venv venv
venv\\Scripts\\activate   # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

# 3. Download models (offline copy)
# Place files in ./models/:
#   crop_disease_model.tflite
#   phi-3-mini-4k-instruct-q4.gguf

# 4. Initialize SQLite database
python -c "from backend.database.models import Base, engine; Base.metadata.create_all(bind=engine)"

# 5. Run backend
uvicorn backend.main:app --reload --port 8000

# 6. Run frontend (in separate terminal)
cd frontend
npm install
npm run dev
```

### Docker (Recommended)

```bash
docker compose up --build
```

### Offline Deployment

```bash
# Backend as standalone binary
pyinstaller --onefile --add-data "models:models" backend/main.py

# Frontend as static PWA
npm run build
# Serve ./frontend/build/ via any static server
```

## Future Scope

- **Mobile App** – Native Android/iOS build using Flutter with on-device TFLite + llama.cpp bindings.
- **Multilingual LLM** – Replace Phi-3 with a multilingual GGUF for regional language recommendations.
- **Drone / IoT Integration** – Capture images from field cameras for continuous inference.
- **Community Knowledge Graph** – Local knowledge base with region-specific pest data.
- **Federated Learning** – Periodic model updates without exchanging raw data.
- **IoT Edge Device Packaging** – Raspberry Pi 5 appliance for village centers.
- **SMS Fallback** – USSD / SMS integration for feature-phone users.
- **Yield Prediction** – Add regression model to estimate financial loss from disease severity.

## Why This Project Fits the Hackathon

| Criterion | How AgriGuard AI Delivers |
|-----------|---------------------------|
| **Offline Resilience** | Zero network calls. All models, prompts, and DB are local. |
| **CPU Efficiency** | TFLite CPU delegate + 4-bit GGUF weights. No GPU required. |
| **Structured Data Extraction** | Pydantic-enforced JSON schemas for every diagnosis and recommendation. |
| **Accuracy** | Quantized EfficientNet-MobileNet backbone + LLM post-processing for explainability. |
| **User Experience** | Responsive PWA, camera-first, dark-mode UI, instant results. |

## License

GNU Affero General Public License v3.0 or later — see [LICENSE](LICENSE).

## Contact

AgriGuard AI Team — [GitLab Repository](https://code.swecha.org/yeshu_09/agriguard-ai)

