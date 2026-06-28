# Work Division Plan — AgriGuard AI Phase 1

## Team Composition

| Role | Name | Responsibility | Estimated Workload |
|------|------|----------------|-------------------|
| **Team Lead** | [TBD] | Architecture, integration, CI/CD, Hackathon submission | 25% |
| **Backend Developer** | [TBD] | FastAPI, SQLite, API endpoints, pipeline orchestration | 30% |
| **AI/ML Engineer** | [TBD] | Model selection, TFLite conversion, OpenCV, llama.cpp | 25% |
| **Frontend Developer** | [TBD] | Responsive UI, camera capture, offline PWA | 20% |

---

## Team Lead (25%)

### Responsibilities
- Define system architecture and approve all interfaces (API contracts, DB schema, JSON schemas).
- Set up GitLab repository, CI/CD, branch protection, and merge request templates.
- Coordinate daily syncs, track sprint progress, and resolve blockers.
- Integrate backend, frontend, and AI components into a working end-to-end pipeline.
- Package application for offline deployment (PyInstaller + Docker).
- Prepare Hackathon Phase 1 submission materials (README, docs, demo, video).
- Conduct final code review and bug bash before submission.

### Key Deliverables
- `README.md` and all Phase 1 documentation in `docs/`.
- `.gitlab-ci.yml` and build scripts.
- Final integrated application bundle.
- Demo video and submission package.

---

## Backend Developer (30%)

### Responsibilities
- Design and implement SQLAlchemy ORM models, migrations, and CRUD helpers.
- Build FastAPI routers: `/api/v1/diagnose`, `/api/v1/history`, `/api/v1/stats`, `/api/v1/export`, `/api/v1/health`.
- Write Pydantic DTOs and enforce JSON schema validation on all I/O.
- Implement OpenCV preprocessing service (`preprocessor.py`).
- Create TensorFlow Lite inference wrapper (`tflite_inference.py`).
- Build llama.cpp service wrapper (`llm_service.py`) with CPU-only execution.
- Write pytest suites for preprocessing, inference, DB, and API layers.
- Manage `requirements.txt` and ensure reproducible environments.

### Key Deliverables
- `backend/main.py` with all routers registered.
- `backend/services/*` modules.
- `backend/tests/` with ≥ 70% coverage.
- `database/schema.sql`.

---

## AI/ML Engineer (25%)

### Responsibilities
- Curate, augment, and validate the crop-disease dataset for model training.
- Train or fine-tune a lightweight CNN (e.g., EfficientNet-B0, MobileNetV2) for leaf disease classification.
- Convert the trained model to TensorFlow Lite format (`.tflite`).
- Run post-training quantization (int8 / float16) and validate accuracy (target ≥ 85%).
- Configure model input resolution (224×224 or 320×320) and normalization parameters.
- Integrate llama.cpp with Phi-3 Mini 4-bit GGUF; tune generation parameters (temperature, top-p, max tokens).
- Design JSON grammar or Pydantic schema to enforce structured LLM output.
- Write integration tests covering preprocessing → inference → LLM → DB.

### Key Deliverables
- `models/crop_disease_model.tflite` with accompanying `labels.txt`.
- `models/phi-3-mini-4k-instruct-q4.gguf` (downloaded/placed).
- `backend/services/preprocessor.py`, `tflite_inference.py`, `llm_service.py`.
- Accuracy benchmarks and latency profiling report.

---

## Frontend Developer (20%)

### Responsibilities
- Create responsive offline-first UI shell using HTML5 + Tailwind CSS + Vanilla JS.
- Implement webcam capture flow (`getUserMedia`) and file upload input with preview.
- Build diagnosis result card with disease label, confidence visualization, and collapsible structured recommendations.
- Develop history gallery with masonry/grid layout, date/crop/disease filters, and stats widget.
- Implement JSON / CSV export from frontend and offline PWA service worker caching.
- Ensure full responsiveness from 320 px width to wide desktop screens.
- Write Vitest / Jest tests for components, API client, and offline fallback states.
- Create sample images and frontend assets (`assets/`, `images/`).

### Key Deliverables
- `frontend/index.html`, `frontend/src/js/`, `frontend/src/css/`.
- Production build in `frontend/build/`.
- `images/sample_01.jpg`, `images/sample_02.jpg`.
- Frontend component tests.

---

## Workload Balance Summary

| Week | Team Lead | Backend Developer | AI/ML Engineer | Frontend Developer |
|------|-----------|-------------------|----------------|--------------------|
| **Days 1–2** | 40% (setup, docs) | 30% (DB schema, routes) | 30% (dataset, model plan) | 0% |
| **Days 3–4** | 20% (reviews) | 30% (preprocessing, TFLite wrapper) | 50% (model training, conversion) | 0% |
| **Days 5–6** | 15% (CI, integration) | 35% (API orchestration, llama.cpp) | 25% (LLM tuning) | 25% (UI shell, camera) |
| **Days 7–8** | 15% (monitoring) | 25% (export, stats, tests) | 15% (pipeline tests) | 45% (dashboard, polishing) |
| **Days 9–10** | 100% (packaging, submission) | 20% (bug fixes) | 10% (final validation) | 10% (final assets) |

## Collaboration Touchpoints

| Event | Frequency | Participants |
|-------|-----------|--------------|
| **Daily Standup** | Every morning | All 4 members (15 min) |
| **API Contract Review** | Day 3 | Backend + AI/ML + Frontend |
| **Model Accuracy Review** | Day 5 | AI/ML + Team Lead |
| **Integration Dry-Run** | Day 8 | All 4 members |
| **Bug Bash + Polish** | Day 9 | All 4 members |
| **Submission Review** | Day 10 | All 4 members |
