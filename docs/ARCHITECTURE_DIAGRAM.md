# Architecture Diagram — AgriGuard AI

## ASCII Pipeline Architecture

```
┌───────────────────────────────────────────────────────────────────────────┐
│                        OFFLINE CPU-ONLY PIPELINE                            │
└───────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │   Leaf Image     │
    │ (JPG / PNG / BMP)│
    └────────┬─────────┘
             │  upload / camera
             ▼
    ┌──────────────────┐
    │   OpenCV         │
    │  Preprocessor    │
    │  • Resize        │
    │  • BGR → RGB     │
    │  • Normalize     │
    │  • Edge enhance  │
    └────────┬─────────┘
             │  numpy.ndarray
             ▼
    ┌──────────────────┐
    │ TensorFlow Lite  │
    │      Model       │
    │  (CPU delegate)  │
    │                   │
    │  Output:         │
    │  • disease       │
    │  • confidence    │
    │  • top-3 scores  │
    └────────┬─────────┘
             │  prediction
             ▼
    ┌──────────────────┐
    │   Prompt Builder │
    │                   │
    │  "Disease: X     │
    │  Crop: Y         │
    │   give JSON..."  │
    └────────┬─────────┘
             │  prompt
             ▼
    ┌──────────────────────────┐
    │   Phi-3 Mini (llama.cpp) │
    │   • 4-bit GGUF           │
    │   • CPU threads          │
    │   • temp 0.3             │
    │   • max_tokens 512       │
    │                          │
    │   Output:                │
    │   structured JSON        │
    └────────┬─────────────────┘
             │  JSON text
             ▼
    ┌──────────────────────────┐
    │   JSON Validator         │
    │   (Pydantic schema)      │
    │                          │
    │   • parse                │
    │   • enforce types        │
    │   • reject malformed     │
    └────────┬─────────────────┘
             │  DiagnosisReport
             ▼
    ┌──────────────────────────┐
    │      SQLite Storage      │
    │   • diagnoses            │
    │   • images               │
    │   • recommendation_log   │
    │   • FTS5 search          │
    └────────┬─────────────────┘
             │  query / export
             ▼
    ┌──────────────────────────┐
    │   Responsive Dashboard   │
    │   • Gallery              │
    │   • History              │
    │   • Stats                │
    │   • Export JSON / CSV    │
    └──────────────────────────┘
```

## Component Detail

### 1. Leaf Image
- Source: file upload or `getUserMedia` webcam capture.
- Formats: JPEG, PNG, BMP.
- Max size: 10 MB.

### 2. OpenCV Preprocessor
- Library: `opencv-python`.
- Operations:
  - `cv2.imdecode` to read bytes into `BGR` matrix.
  - `cv2.resize` with `INTER_AREA` to 224×224 or 320×320.
  - `cv2.cvtColor(img, COLOR_BGR2RGB)`.
  - Normalize: divide by 255.0 → `float32` in `[0, 1]`.
  - Optional: Canny edge map overlay for robustness.

### 3. TensorFlow Lite Model
- File: `models/crop_disease_model.tflite`.
- Runtime: `tf.lite.Interpreter` with CPU threads pinned to physical cores.
- Quantization: INT8 or float16.
- Output: `(class_id, confidence)` for top-3 predictions.

### 4. Prompt Builder
- Template: disease class name + crop type + schema instructions.
- Enforced output via llama.cpp grammar or Pydantic post-parse.

### 5. Phi-3 Mini (llama.cpp)
- File: `models/phi-3-mini-4k-instruct-q4.gguf`.
- Runtime: llama.cpp Python bindings on CPU.
- Parameters: `temperature=0.3`, `top_p=0.9`, `max_tokens=512`, `n_threads=auto`.

### 6. JSON Validator
- Schema: `DiagnosisReport` Pydantic model.
- Retry policy: up to 2 regeneration attempts if schema validation fails.

### 7. SQLite Storage
- Schema: `diagnoses`, `images`, `recommendation_history`.
- FTS5 virtual table for offline full-text search.

### 8. Responsive Dashboard
- Frontend: HTML5 + Tailwind CSS + Vanilla JS.
- Features: gallery grid, filters, stats cards, export buttons.
- Offline: service worker caches shell + API responses.

## Data Flow Summary

| Step | Format | Owner |
|------|--------|-------|
| Capture | bytes (multipart) | Frontend |
| Preprocess | numpy.ndarray | Preprocessor |
| Inference | dict (top-K) | TFLite wrapper |
| LLM | text → JSON | LLM service |
| Validate | Pydantic model | Report builder |
| Store | SQLite rows | DB layer |
| Display | JSON payload | Frontend |
