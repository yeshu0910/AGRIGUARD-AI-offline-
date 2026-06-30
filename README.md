# AgriGuard AI – Offline Crop Disease Logger

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-AGPLv3-green)
![Platform](https://img.shields.io/badge/platform-offline_only-red)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen)

## Project Overview

**AgriGuard AI** is a fully offline, CPU-first artificial intelligence application designed to detect crop diseases from leaf images without any internet connection. Built for farmers, extension officers, and agricultural researchers, it empowers users to diagnose plant health instantly using a smartphone or laptop, regardless of network availability.

The application combines a TensorFlow Lite classification model running on-device with a local small language model (Phi-3 Mini GGUF via llama.cpp) to generate structured, actionable treatment recommendations. All inference, storage, and reporting happen locally on CPU.

## Problem Statement

Over 500 million smallholder farmers worldwide lose 20–40% of crop yield annually to pests and diseases. Existing digital agri-advisory services require internet, smartphones with data plans, and cloud subscriptions — barriers that exclude the most vulnerable farming communities. Extension officers and farmers in rural areas often wait days for expert advice, by which time the disease has spread irreversibly.

There is an urgent need for an **offline, zero-cost, privacy-preserving** diagnostic tool that runs on commodity hardware.

## Solution

AgriGuard AI provides a complete offline AI pipeline:

1. **Ingest** – Farmer or extension officer captures a leaf photo via the offline web interface.
2. **Preprocess** – OpenCV normalizes the image (resize, color space, optional leaf extraction).
3. **Classify** – A quantized TensorFlow Lite model runs on CPU to identify the disease.
4. **Recommend** – A local LLM (Phi-3 Mini, 4-bit GGUF) generates structured JSON treatment steps.
5. **Store** – SQLite persists the diagnosis, confidence score, and recommendations locally.
6. **Report** – A responsive dashboard lists history, trends, and exportable reports.

No data leaves the device. No API keys, no cloud, no network required.

## Features

- 100% Offline – No internet, no cloud APIs, no OpenAI.
- CPU-Only Inference – Optimized for Intel/AMD/ARM processors.
- Responsive Web UI – Works on phones, tablets, and desktops.
- Local LLM Recommendations – Phi-3 Mini via llama.cpp gives structured advice.
- 30 Supported Crops – Automatic class discovery from dataset folder structure.
- SQLite History – Full audit trail with timestamp, image path, and confidence.
- JSON/CSV Export – Machine-readable reports for integration or printing.
- Privacy First – All data stays on-device.
- RESTful API – FastAPI endpoints for programmatic access.
- Docker Support – Multi-stage build for production deployment.

## Architecture

```
Leaf Image
    ↓
OpenCV Preprocessing (resize, normalize, leaf extraction)
    ↓
TensorFlow Lite Model (quantized, CPU delegate)
    ↓
Phi-3 Mini (llama.cpp, 4-bit GGUF)
    ↓
JSON Report (severity, treatment, prevention)
    ↓
SQLite Storage (WAL mode)
    ↓
Responsive Dashboard (history, filters, export)
```

| Component | Role |
|-----------|------|
| Leaf Image | User-captured photo of affected crop |
| OpenCV | Resize, normalize, edge enhancement, leaf region extraction |
| TensorFlow Lite | On-device disease classification |
| Phi-3 Mini (llama.cpp) | Local LLM generates structured recommendations |
| Knowledge Base | Curated fallback recommendations for 14 crop-disease pairs |
| JSON Report | Structured output with confidence & advice |
| SQLite | Persistent offline storage with WAL mode |
| Dashboard | Gallery, filters, history, export |

## Supported Crops

AgriGuard AI supports **30 crops** with automatic class discovery. The model detects both diseases and healthy plants for each crop.

| # | Crop | Diseases Covered |
|---|------|-----------------|
| 1 | Tomato | Bacterial spot, Early blight, Late blight, Leaf mold, Septoria leaf spot, Spider mites, Target spot, Mosaic virus, Yellow leaf curl virus |
| 2 | Potato | Early blight, Late blight |
| 3 | Maize / Corn | Cercospora leaf spot, Common rust, Northern leaf blight |
| 4 | Rice | Blast, Brown spot, Tungro |
| 5 | Wheat | Brown rust, Yellow rust, Septoria |
| 6 | Cotton | Aphid, Bacterial blight, Fusarium wilt, Leaf spot |
| 7 | Soybean | Bacterial blight, Frog eye leaf spot, Rust |
| 8 | Pepper | Bacterial spot |
| 9 | Apple | Apple scab, Black rot, Cedar apple rust |
| 10 | Grape | Black rot, Esca, Leaf blight |
| 11 | Banana | Black Sigatoka, Panama wilt |
| 12 | Mango | Anthracnose, Powdery mildew |
| 13 | Sugarcane | Red rot, Smut |
| 14 | Chili | Anthracnose, Leaf spot, Powdery mildew |
| 15 | Onion | Downy mildew, Purple blotch |
| 16 | Garlic | Downy mildew, Rust |
| 17 | Cabbage | Black rot, Clubroot |
| 18 | Cauliflower | Black rot, Downy mildew |
| 19 | Brinjal / Eggplant | Fruit borer, Leaf spot, Powdery mildew |
| 20 | Cucumber | Downy mildew, Powdery mildew |
| 21 | Pumpkin | Downy mildew, Powdery mildew |
| 22 | Groundnut / Peanut | Early leaf spot, Late leaf spot, Rust |
| 23 | Mustard | Alternaria blight, Powdery mildew |
| 24 | Sunflower | Downy mildew, Rust |
| 25 | Barley | Net blotch, Powdery mildew, Rust |
| 26 | Millet | Blast, Downy mildew |
| 27 | Pea | Downy mildew, Powdery mildew |
| 28 | Watermelon | Anthracnose, Powdery mildew |
| 29 | Papaya | Anthracnose, Powdery mildew, Ring spot virus |
| 30 | Citrus (Orange/Lemon) | Canker, Greening, Scab |

Each crop includes a **Healthy** class. Classes are detected automatically — no code changes needed when adding new crops.

## Dataset Naming Convention

Dataset folders follow the format:

```
Crop___Disease
```

Rules:
- Crop and disease names use underscores (`_`) instead of spaces
- Triple underscores (`___`) separate crop from disease
- No brackets, no special characters

Examples:
```
Tomato___Late_blight
Rice___Blast
Maize_Corn___Common_rust
Citrus_Orange_Lemon___Greening
Groundnut_Peanut___Leaf_spot
```

Dataset tree example:
```
dataset/
├── Apple___Apple_scab/
├── Apple___Black_rot/
├── Apple___Cedar_apple_rust/
├── Apple___Healthy/
├── Tomato___Bacterial_spot/
├── Tomato___Healthy/
├── Tomato___Late_blight/
...
```

### Class Discovery

Classes are **automatically discovered** from folder names at training time:

1. The `DatasetLoader` scans all subdirectories in `dataset/`
2. Each folder name becomes a class label
3. Folder names are sorted deterministically and saved to `models/classes.json`
4. The model output layer size = `len(class_names)` (no hardcoded values)
5. Adding a new crop or disease = adding a new folder — no code changes required

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | HTML5 + Tailwind CSS + Vanilla JS | Responsive offline PWA-capable UI |
| Backend / API | FastAPI (Python) | REST endpoints, CORS, async I/O |
| Image Processing | OpenCV (Python) | Resize, normalize, augment |
| Inference Engine | TensorFlow Lite (Python) | Quantized CPU-only classification |
| LLM Runtime | llama.cpp + Phi-3 Mini GGUF | 4-bit quantized local text generation |
| Database | SQLite3 + SQLAlchemy | Structured schema, WAL mode |
| Serialization | Pydantic v2 | JSON schema validation, API contracts |
| Packaging | Docker / PyInstaller | Portable container or standalone binary |

## Screenshots

> Screenshots will be added to the `assets/` directory. Key views include:
>
> - **Diagnosis Page**: Image upload, camera capture, and result display
> - **Dashboard**: History view with filters by crop, disease, and severity
> - **Report View**: Detailed diagnosis with confidence, severity, and recommendations
> - **Export**: JSON and CSV export functionality

## Model Information

### Disease Classification Model
- **Architecture**: EfficientNetB0 (transfer learning)
- **Format**: Keras / TensorFlow
- **Input Size**: 224×224×3 RGB
- **Output**: Softmax over disease classes (dynamic, based on dataset)
- **Class Discovery**: Automatic — reads folder names from `dataset/`
- **Supported Crops**: 30 crops with 80–150 disease/healthy classes

### Recommendation Model
- **Model**: Phi-3 Mini 4K Instruct
- **Format**: 4-bit GGUF quantized
- **Runtime**: llama.cpp
- **Context**: 2048 tokens
- **Fallback**: Built-in curated knowledge base covering 30 crops and common diseases

## Offline Mode

AgriGuard AI is designed for **complete offline operation**:

- All AI models are stored locally in `models/`
- SQLite database stores all data locally
- No telemetry, no crash reporting, no external API calls
- Frontend assets are served as a static PWA
- Works on any device with Python 3.10+ and a modern browser

To verify offline mode:
```bash
# Block all network access and test
pytest tests/ -k offline
```

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend build, optional)
- CMake 3.18+ (for llama.cpp build, optional)
- Git
- 4 GB RAM minimum (8 GB recommended)
- 2 GB free disk space for models and dependencies

### Quick Start (Development)

```bash
# 1. Clone the repository
git clone <repository-url>
cd agriguard-ai

# 2. Set up Python environment
python -m venv venv
venv\Scripts\activate   # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

# 3. Download models (offline copy)
# Place files in ./models/:
#   crop_disease_model.tflite
#   phi-3-mini-4k-instruct-q4.gguf

# 4. Initialize SQLite database
python -c "from backend.database import init_db; init_db()"

# 5. Run backend
uvicorn AgriGuard.backend.app:app --reload --port 8000

# 6. Run frontend (in separate terminal, optional)
cd frontend
npm install
npm run dev
```

### Docker (Recommended)

```bash
docker build -t agriguard-ai:latest .
docker run --rm -p 8000:8000 -v "$(pwd)/models:/app/models" -v "$(pwd)/database:/app/database" agriguard-ai:latest
```

### Offline Deployment

```bash
# Backend as standalone binary
pyinstaller --onefile --add-data "models:models" backend/main.py

# Frontend as static PWA
npm run build
# Serve ./frontend/build/ via any static server

# Or use Docker for full offline appliance
docker compose up --build
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | System health check |
| POST | `/detect` | Upload image for disease detection |
| GET | `/history` | List diagnosis history (filterable) |
| GET | `/history/{id}` | Get specific diagnosis |
| DELETE | `/history/{id}` | Delete diagnosis record |
| GET | `/export/csv` | Export all records as CSV |
| GET | `/export/json` | Export all records as JSON |
| GET | `/` | Serve frontend SPA |

## Development Guide

### Setup Development Environment

```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Run Quality Checks

```bash
ruff check .                          # Lint with Ruff
ruff format . --check                 # Check formatting with Ruff
mypy backend/                         # Type check
flake8 backend/                       # Style check
pylint backend/                       # Code quality
vulture backend/ --min-confidence 80  # Dead code detection
bandit -qr backend/                   # Security scan
semgrep --config=auto backend/        # SAST scan
pyupgrade --py310-plus **/*.py        # Modernize syntax
pip-audit -r requirements.txt         # Dependency audit
```

### Run Tests

```bash
pytest                          # Run all tests
pytest --cov=backend            # With coverage
pytest -v                       # Verbose output
pytest tests/ -k offline        # Run offline-specific tests
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, development process, and commit conventions.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## License

GNU Affero General Public License v3.0 or later — see [LICENSE](LICENSE).

## Contact

AgriGuard AI Team — [GitLab Repository](mailto:team@example.com)
# AGRIGUARD-AI-offline-
