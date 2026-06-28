# User Manual — AgriGuard AI

## Overview

AgriGuard AI is an offline, CPU-only application that detects crop diseases from leaf images and provides structured treatment recommendations. It is designed for farmers, extension officers, and researchers who need fast, private, and reliable plant health diagnostics without internet access.

## Installation

### Requirements
- Python 3.10+
- Node.js 18+ (frontend build only)
- 4 GB RAM minimum (8 GB recommended)
- 2 GB free disk space for models and dependencies

### Quick Install

```bash
# Clone the repository
git clone <repository-url>
cd agriguard-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```env
APP_ENV=development
LOG_LEVEL=INFO
MODEL_PATH=models/crop_disease_model.tflite
LLM_MODEL_PATH=models/phi-3-mini-4k-instruct-q4.gguf
LABELS_PATH=models/labels.txt
DB_PATH=database/agriguard.db
MAX_UPLOAD_SIZE_MB=10
```

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Runtime environment | `development` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `MODEL_PATH` | Path to TFLite classifier | `models/crop_disease_model.tflite` |
| `LLM_MODEL_PATH` | Path to Phi-3 Mini GGUF | `models/phi-3-mini-4k-instruct-q4.gguf` |
| `LABELS_PATH` | Path to class labels | `models/labels.txt` |
| `DB_PATH` | Path to SQLite database | `database/agriguard.db` |
| `MAX_UPLOAD_SIZE_MB` | Max image size in MB | `10` |

## Running Locally

### Start the Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

### Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

### Access the Application

Open `http://localhost:3000` (frontend) or `http://localhost:8000` (API docs).

## Running with Docker

### Build Image

```bash
docker build -t agriguard-ai:latest .
```

### Run Container

```bash
docker run --rm -p 8000:8000 \\
  -v "$(pwd)/models:/app/models" \\
  -v "$(pwd)/database:/app/database" \\
  agriguard-ai:latest
```

### Access

- API docs: `http://localhost:8000/docs`

> Note: The frontend build output is served statically by the container if present in `frontend/build/`. Otherwise, run the frontend dev server separately on port 3000.

## Common Workflows

### Diagnose a Crop Disease

1. Open the application in your browser.
2. Click the camera icon or upload a leaf image.
3. Wait for processing (typically 2–10 seconds).
4. Review the diagnosis, confidence score, and recommendations.
5. Save the record to history or export as JSON.

### View History

1. Click the History tab.
2. Filter by date, crop type, or disease.
3. Click a record to view full details.

### Export Data

1. Go to History.
2. Click Export JSON or Export CSV.
3. Save the file to your device.

### Offline Usage

- After the first load, the application works without internet.
- Place model files in `models/` before going offline.
- SQLite stores all records locally.

## Troubleshooting

### Camera Not Working
- Ensure the browser has camera permissions.
- Use HTTPS or localhost for camera access.
- On mobile, use the file upload option as a fallback.

### Slow Inference
- Close other CPU-heavy applications.
- Reduce image resolution in preprocessing settings.
- Ensure the TFLite model is quantized (int8/float16).
- Check that llama.cpp is using CPU threads only.

### Model Not Found
- Verify `MODEL_PATH` and `LLM_MODEL_PATH` in `.env`.
- Confirm files exist in the `models/` directory.
- Check file permissions.

### Database Errors
- Ensure the `database/` directory exists.
- Check disk space.
- Delete `agriguard.db` to reset (data will be lost).

### Frontend Not Loading
- Run `npm install` in `frontend/`.
- Clear browser cache.
- Check browser console for errors.

## FAQ

**Q: Does AgriGuard AI send data to the cloud?**
A: No. All inference and storage are local. No data leaves the device.

**Q: What image formats are supported?**
A: JPEG, PNG, and BMP up to 10 MB.

**Q: Can I use this on a phone without internet?**
A: Yes, if hosted locally or packaged as a PWA with cached assets.

**Q: How accurate is the disease detection?**
A: The target accuracy is 85%+ top-1 on the held-out test set. Actual accuracy may vary by crop and image quality.

**Q: What if the LLM produces malformed JSON?**
A: The system retries up to 2 times. If it still fails, the raw text is stored for debugging.

**Q: Can I add my own crop disease model?**
A: Yes. Replace `models/crop_disease_model.tflite` and update `models/labels.txt`.
