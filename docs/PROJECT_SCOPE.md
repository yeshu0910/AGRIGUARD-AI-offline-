# Project Scope — AgriGuard AI

## In Scope (Phase 1)

### Core Application
- Offline image capture and upload via responsive web interface.
- OpenCV-based preprocessing (resize, color conversion, normalization).
- TensorFlow Lite CPU-only disease classification.
- Phi-3 Mini 4-bit GGUF local LLM inference via llama.cpp.
- Structured JSON report generation with Pydantic validation.
- SQLite persistent storage with FTS5 full-text search.
- History gallery with date, crop, and disease filtering.
- Export to JSON and CSV formats.
- Offline-first frontend with service worker caching.

### AI / ML
- Quantized TensorFlow Lite model for crop disease classification.
- Local LLM integration restricted to llama.cpp runtime.
- Strict JSON schema enforcement for LLM outputs.
- Accuracy benchmark ≥ 85% top-1 on held-out test set.

### Backend
- FastAPI REST API with CORS and async support.
- SQLAlchemy ORM for database interactions.
- Multipart image upload handling.
- End-to-end pipeline integration tests.
- Unit tests for preprocessing, inference, LLM, and API layers.

### Frontend
- Responsive layout targeting 320 px – 1920 px+.
- Camera capture using `getUserMedia` API.
- File upload with client-side preview.
- Diagnosis result card with confidence visualization.
- History gallery with filter and sort capabilities.
- PWA-ready service worker for offline caching.

### DevOps & Submission
- GitLab repository with CI/CD pipeline.
- Docker containerization and PyInstaller packaging.
- Documentation suite (README, specs, timeline, issues, etc.).
- Demo screenshots and 3-minute demo video.
- Phase 1 submission checklist.

---

## Out of Scope (Phase 1)

The following features are explicitly excluded from Phase 1 to maintain focus:

- **Cloud APIs** – No OpenAI API, no Hugging Face Inference API, no cloud storage (S3, Firebase, etc.).
- **GPU Acceleration** – No CUDA, ROCm, Vulkan, or Metal acceleration. CPU-only execution only.
- **Real-Time Video Stream** – Single static image diagnosis only; live video feed is a Phase 2 feature.
- **Multi-User Auth** – No user accounts, roles, or permissions. Single-device, single-user usage.
- **GPS / Location Services** – No automatic geotagging or mapping features.
- **SMS / USSD Integration** – Feature-phone text-based access is deferred.
- **Federated Learning** – No model update distribution to edge devices.
- **Mobile Native Apps** – No Flutter, React Native, or native iOS/Android builds.
- **Drone / IoT Hardware** – No integration with field cameras or IoT sensors.
- **Predictive Analytics** – No yield forecasting, weather integration, or economic impact modeling.
- **Multilingual LLM** – English-only recommendations in Phase 1.
- **E-Commerce / Payments** – No marketplace for pesticides or seeds.

---

## Future Enhancements (Phase 2 and beyond)

### Near-Term (Phase 2)
- **Multilingual Support** – Fine-tune or replace Phi-3 with a multilingual GGUF for regional-language recommendations.
- **Mobile Wrapper** – Wrap the PWA in a Capacitor or Flutter shell for app-store distribution.
- **SMS Fallback** – USSD or SMS gateway for basic feature-phone access.
- **Improved Model Accuracy** – Ensemble TFLite with a secondary model (e.g., ViT-based classifier) for > 90% accuracy.
- **Drone Image Batch Processing** – Accept zip archives of drone-captured field images and run batch diagnosis.

### Mid-Term (Phase 3)
- **Federated Learning** – Periodic model updates without transmitting raw field data.
- **IoT Edge Appliance** – Package as a Raspberry Pi 5 device for village agri-kiosks.
- **Community Knowledge Graph** – Local RAG system with region-specific pest and pesticide database.
- **Yield Impact Estimation** – Regression model to predict financial loss from disease severity and progress.

### Long-Term (Phase 4+)
- **Multi-Crop Specialization** – Domain-adapt models for rice, wheat, maize, cotton, etc.
- **Drone Swarm Integration** – Autonomous field scouting with real-time disease mapping.
- **Supply Chain Linkage** – Direct connections to pesticide suppliers and extension services.
- **Farmer Cooperative Networks** – Shared anonymous diagnosis data pools for regional trend analysis (with opt-in privacy controls).

---

## Scope Change Control

Any scope changes requested during development must be:
1. Logged as a GitLab issue labeled `scope-change`.
2. Evaluated against the 10-day Phase 1 timeline.
3. Accepted only if it does not compromise the 5 core deliverables (README, API, UI, models, tests).
4. Approved by the Team Lead and documented in `PROJECT_TIMELINE.md`.
