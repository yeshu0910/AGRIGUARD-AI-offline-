# Folder Structure — AgriGuard AI

```
AgriGuard_AI/
├── .git/                            # Git repository data
├── .gitignore                       # Ignore rules for venv, build artifacts, models, DB
├── LICENSE                          # MIT License
├── README.md                        # Main project README
├── requirements.txt                 # Python runtime dependencies
├── requirements-dev.txt             # Python testing & linting dependencies
├── pyproject.toml                   # Build system metadata (PEP 621)
├── SUBMISSION.md                    # Hackathon submission checklist
│
├── backend/                         # FastAPI backend application
│   ├── __init__.py
│   ├── main.py                      # Uvicorn / FastAPI app factory
│   ├── config.py                    # Settings (paths, model versions, thread counts)
│   │
│   ├── database/                    # Database layer
│   │   ├── __init__.py
│   │   ├── engine.py                # SQLAlchemy engine + session factory
│   │   ├── models.py                # ORM classes: Diagnosis, Image, RecommendationHistory
│   │   ├── schemas.py               # Pydantic DTOs: DiagnosisCreate, DiagnosisReport, Stats
│   │   ├── crud.py                  # Create, read, update, delete helpers
│   │   └── migrate.py               # Optional migration runner
│   │
│   ├── routers/                     # API route modules
│   │   ├── __init__.py
│   │   ├── disease.py               # POST /api/v1/diagnose
│   │   ├── history.py               # GET/DELETE /api/v1/history, /api/v1/history/{id}
│   │   ├── stats.py                 # GET /api/v1/stats
│   │   └── export.py                # GET /api/v1/export/json, /api/v1/export/csv
│   │
│   ├── services/                    # Business logic & external tool wrappers
│   │   ├── __init__.py
│   │   ├── preprocessor.py          # OpenCV: decode, resize, normalize, edge-enhance
│   │   ├── tflite_inference.py      # TF Lite interpreter wrapper (CPU delegate)
│   │   ├── llm_service.py           # llama.cpp + Phi-3 Mini GGUF wrapper
│   │   └── report_builder.py        # Assemble DiagnosisReport + optional PDF
│   │
│   └── tests/                       # Backend tests
│       ├── __init__.py
│       ├── test_preprocessing.py    # OpenCV unit tests
│       ├── test_inference.py        # TF Lite wrapper tests
│       ├── test_llm.py              # llama.cpp unit tests
│       └── test_api.py              # FastAPI TestClient integration tests
│
├── frontend/                        # Offline-first responsive web app
│   ├── index.html                   # SPA shell
│   ├── package.json                 # Node dependencies
│   ├── tailwind.config.js           # Tailwind CSS configuration
│   ├── postcss.config.js            # PostCSS configuration
│   │
│   ├── src/
│   │   ├── css/
│   │   │   └── main.css             # Custom styles beyond Tailwind
│   │   ├── js/
│   │   │   ├── app.js               # Entry point
│   │   │   ├── api.js               # fetch wrappers + error handling
│   │   │   ├── camera.js            # getUserMedia + canvas capture
│   │   │   ├── gallery.js           # History grid, filters, card components
│   │   │   └── dashboard.js         # Stats widgets + export buttons
│   │   └── assets/
│   │       ├── icons/               # SVG icons
│   │       └── images/              # Demo images, logo
│   │
│   └── build/                       # Production build output (gitignored)
│
├── models/                          # Local AI model artifacts (gitignored, large)
│   ├── crop_disease_model.tflite    # Quantized classifier
│   ├── labels.txt                   # Label index
│   └── phi-3-mini-4k-instruct-q4.gguf  # 4-bit LLM weights
│
├── database/                        # Database files
│   ├── schema.sql                   # Human-readable DDL
│   └── agriguard.db                 # Runtime SQLite file (gitignored)
│
├── images/                          # Sample / demo images
│   ├── sample_01.jpg
│   ├── sample_02.jpg
│   └── README_images.md             # Licensing & attribution
│
├── assets/                          # Branding & static assets
│   ├── logo.svg
│   └── favicon.ico
│
├── docs/                            # Phase 1 documentation (Markdown)
│   ├── README.md
│   ├── SPECIFICATION_KIT.md
│   ├── GITLAB_ISSUES.md
│   ├── WORK_DIVISION_PLAN.md
│   ├── PROJECT_TIMELINE.md
│   ├── DELIVERABLES.md
│   ├── FOLDER_STRUCTURE.md          # This file
│   ├── ARCHITECTURE_DIAGRAM.md
│   ├── PROJECT_SCOPE.md
│   └── HACKATHON_ALIGNMENT.md
│
├── tests/                           # Cross-layer integration tests
│   └── integration/
│       └── test_pipeline.py         # Image → TF Lite → LLM → SQLite → JSON
│
├── build/                           # Deployment bundles
│   ├── agriguard-ai.exe
│   ├── agriguard-ai-linux
│   └── agriguard-ai.docker
│
├── demo/                            # Hackathon demo artifacts
│   ├── screenshots/
│   │   ├── mobile_home.png
│   │   ├── mobile_result.png
│   │   └── desktop_dashboard.png
│   └── demo_video.mp4               # 3-minute demo recording
│
└── reports/                         # Validation & benchmark outputs
    ├── accuracy_benchmark.txt
    └── coverage.xml                 # pytest-cov HTML or XML report
```

| Indicator | Meaning |
|-----------|---------|
| `gitignored` | File is in `.gitignore` (too large or environment-specific) |
| `binary` | Model or image file; not human-readable |
| `generated` | Created by build scripts, not committed directly |
