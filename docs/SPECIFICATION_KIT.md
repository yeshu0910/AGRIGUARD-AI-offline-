# Specification Kit — AgriGuard AI

## Objective

Deliver a fully offline, CPU-only AI-powered crop disease diagnosis application that classifies leaf images using a quantized TensorFlow Lite model and produces structured treatment recommendations via a local Small Language Model (Phi-3 Mini GGUF through llama.cpp). The system must store all outputs in a local SQLite database and expose a responsive offline-first interface.

## Users

| Persona | Description | Key Needs |
|---------|-------------|-----------|
| **Smallholder Farmer** | Low-literacy user in remote area with Android feature phone or basic laptop. | Point-and-shoot diagnosis, simple language, offline access. |
| **Agricultural Extension Officer** | Government / NGO worker visiting villages with a tablet or laptop. | Batch logging, exportable reports, historical trends. |
| **Researcher / Student** | Agronomy student or researcher collecting field data. | Structured JSON exports, metadata accuracy, reproducibility. |

## Functional Requirements

### FR-1: Image Ingestion
- The system shall accept leaf images via file upload (`multipart/form-data`) or webcam capture.
- Supported formats: JPEG, PNG, BMP.
- Maximum file size: 10 MB per image.

### FR-2: Image Preprocessing
- The system shall resize images to the model input resolution (e.g., 224×224 or 320×320).
- The system shall convert BGR to RGB (OpenCV default) and normalize pixel values.
- The system may apply edge enhancement (Canny / bilateral filter) as a preprocessing option.

### FR-3: Offline Disease Classification
- The system shall load a TensorFlow Lite model (`.tflite`) optimized for CPU execution.
- The model shall be invoked without any network call.
- The system shall return the top-3 predicted disease classes with confidence scores.

### FR-4: Local LLM Recommendation
- The system shall prompt a local GGUF LLM (Phi-3 Mini) with the predicted disease class and crop type.
- The LLM shall be executed via llama.cpp on CPU threads only.
- The system shall enforce structured JSON output schema (see JSON Schema section).
- No external API may be invoked to coerce formatting (e.g., no OpenAI Function Calling proxy).

### FR-5: Structured JSON Report
- Each diagnosis shall produce a JSON object containing a unique ID, timestamp, input image reference, predicted disease, confidence scores, and LLM-generated recommendations.

### FR-6: SQLite Persistence
- The system shall persist every diagnosis record in SQLite.
- The system shall support full-text search across disease names, crop types, and notes.

### FR-7: History & Dashboard
- The system shall display a gallery of past diagnoses.
- The user shall be able to filter by date range, crop type, or disease.
- The user shall export records as JSON or CSV.

### FR-8: Offline Responsive UI
- The frontend shall function without an active internet connection after initial load (service worker cache).
- The UI shall be responsive from 320 px width to 1920 px+.

## Non-Functional Requirements

| ID | Requirement | Metric |
|----|-------------|--------|
| NFR-1 | Offline-only operation | 0 outbound network connections during runtime |
| NFR-2 | CPU-only inference | Runs on 4-core CPU, no CUDA / ROCm / Vulkan |
| NFR-3 | End-to-end latency | < 10 seconds per diagnosis on 4-core CPU |
| NFR-4 | Model accuracy | Top-1 accuracy ≥ 85% on held-out test set |
| NFR-5 | Data privacy | No telemetry, no crash reporting to third parties |
| NFR-6 | Portability | Backend packaged as single exe (PyInstaller) or Docker image |
| NFR-7 | Frontend load size | < 5 MB initial payload (service worker cache strategy) |
| NFR-8 | Database scalability | Handles 10,000+ records without degradation |

## Offline AI Pipeline

```
Input Image
   │
   ▼
OpenCV Preprocessor   (resize, color convert, normalize)
   │
   ▼
TensorFlow Lite       (CPU delegate, int8 / float32 quantized)
   │
   ▼
Phi-3 Mini GGUF       (llama.cpp, 4-bit quantized, CPU threads)
   │
   ▼
Structured JSON       (disease label, confidence, recommendations)
   │
   ▼
SQLite Storage        (append diagnosis + metadata)
```

## Input

| Attribute | Specification |
|-----------|---------------|
| Format | JPEG, PNG, BMP |
| Color space | RGB / BGR accepted, converted to RGB internally |
| Resolution | Any (resized/centercropped to model input) |
| File size limit | 10 MB |
| Metadata | Optional GPS / timestamp from EXIF (EXIF retained or stripped per privacy config) |

## Processing

| Stage | Tool | Config |
|-------|------|--------|
| Image I/O | OpenCV | `cv2.imdecode` |
| Resize | OpenCV | `INTER_AREA` to 224×224 or 320×320 |
| Color convert | OpenCV | `COLOR_BGR2RGB` |
| Normalize | NumPy | 0–1 float32 or zero-mean std normalization |
| Inference | TensorFlow Lite | `tf.lite.Interpreter`, 1 thread per physical core |
| Fallback | OpenCV DNN (optional) | ONNX model if `.tflite` unavailable |
| Text generation | llama.cpp | 4-bit Phi-3 Mini GGUF, temperature 0.3, max tokens 512 |
| JSON enforcement | Pydantic / Llama.cpp grammar | Strict JSON schema validation |
| Storage | SQLAlchemy + SQLite | ACID, FTS5 virtual table for search |

## Output

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DiagnosisReport",
  "type": "object",
  "required": ["id", "timestamp", "disease", "confidence", "recommendations", "meta"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "input_image": { "type": "string" },
    "disease": { "type": "string" },
    "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "top_predictions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["label", "score"],
        "properties": {
          "label": { "type": "string" },
          "score": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
        }
      }
    },
    "recommendations": {
      "type": "object",
      "required": ["immediate_actions", "chemical_treatment", "organic_alternatives", "prevention", "safety_notes"],
      "properties": {
        "immediate_actions": { "type": "array", "items": { "type": "string" } },
        "chemical_treatment": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["product", "dosage", "method"]
          }
        },
        "organic_alternatives": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["product", "dosage", "method"]
          }
        },
        "prevention": { "type": "array", "items": { "type": "string" } },
        "safety_notes": { "type": "array", "items": { "type": "string" } }
      }
    },
    "meta": {
      "type": "object",
      "required": ["model_version", "inference_ms", "llm_model"]
    }
  }
}
```

## Database Schema

```sql
CREATE TABLE diagnoses (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    image_path TEXT,
    disease TEXT NOT NULL,
    confidence REAL NOT NULL,
    top_predictions TEXT,
    recommendations TEXT,
    meta TEXT,
    crop_type TEXT,
    location TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE diagnoses_fts USING fts5(
    disease, crop_type, location, notes,
    content=diagnoses, content_rowid=rowid
);

CREATE TABLE images (
    id TEXT PRIMARY KEY,
    diagnosis_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    mime_type TEXT,
    size_bytes INTEGER,
    width INTEGER,
    height INTEGER,
    FOREIGN KEY (diagnosis_id) REFERENCES diagnoses(id) ON DELETE CASCADE
);

CREATE TABLE recommendation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diagnosis_id TEXT NOT NULL,
    prompt_template TEXT,
    raw_response TEXT,
    parsed_json TEXT,
    latency_ms INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (diagnosis_id) REFERENCES diagnoses(id) ON DELETE CASCADE
);
```

## API Endpoints

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| `POST` | `/api/v1/diagnose` | Classify image + generate recommendations | `multipart/form-data` (image file) | `DiagnosisReport` |
| `GET` | `/api/v1/history` | List past diagnoses | Query params: `limit`, `offset`, `crop_type`, `date_from`, `date_to` | `List[DiagnosisSummary]` |
| `GET` | `/api/v1/history/{id}` | Retrieve a single diagnosis by ID | — | `DiagnosisReport` |
| `DELETE` | `/api/v1/history/{id}` | Delete a diagnosis and associated image | — | `204 No Content` |
| `GET` | `/api/v1/stats` | Aggregate statistics (disease counts, avg confidence) | Query params: `group_by` | `StatsResponse` |
| `GET` | `/api/v1/export/json` | Export all diagnoses as JSON | Query params: `limit`, `offset` | `application/json` |
| `GET` | `/api/v1/export/csv` | Export all diagnoses as CSV | Query params: `limit`, `offset` | `text/csv` |
| `GET` | `/api/v1/health` | Health check (model loaded, DB connection) | — | `HealthResponse` |

### Health Response Schema

```json
{
  "status": "ok",
  "model_loaded": true,
  "llm_loaded": true,
  "db_connected": true,
  "cpu_count": 4
}
```

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Model size exceeds device storage | Medium | High | Use 4-bit / 8-bit quantized Phi-3; allow external USB storage. |
| CPU inference too slow for UX | Medium | Medium | Pre-warm model at startup; use CPU delegate; show loading progress. |
| LLM produces malformed JSON | High | Medium | Strict grammar / Pydantic validation with retry prompt. |
| SQLite concurrent writes | Low | Medium | Serialize writes via FastAPI dependency; WAL mode. |
| Frontend PWA cache invalidation | Medium | Low | Versioned cache busting; fallback to runtime cache API. |
| Model accuracy below threshold | Medium | High | Data augmentation; ensemble with secondary model; prompt engineer explanation. |

## Success Metrics

| Metric | Target |
|--------|--------|
| Top-1 disease accuracy | ≥ 85% on held-out test set |
| End-to-end latency (CPU, 4-core) | ≤ 10 seconds |
| Offline uptime | 100% of runtime (no network calls logged) |
| JSON schema compliance | 100% of LLM outputs parse successfully |
| Frontend Lighthouse PWA score | ≥ 80 |
| Code coverage (unit tests) | ≥ 70% |
| Issue resolution time | ≤ 48 hours for P0/P1 bugs |
| Hackathon judging criteria met | All 5 criteria satisfied with evidence |
