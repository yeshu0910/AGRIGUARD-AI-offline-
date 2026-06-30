# User Manual — AgriGuard AI

## Overview

AgriGuard AI is an offline, CPU-only application that detects crop diseases from leaf images and provides structured treatment recommendations. It is designed for farmers, extension officers, and researchers who need fast, private, and reliable plant health diagnostics without internet access.

The system uses a TensorFlow Lite model for disease classification and a local language model (Phi-3 Mini via llama.cpp) to generate actionable treatment advice. All data stays on your device — nothing is sent to the cloud.

## System Requirements

- **Operating System**: Windows 10+, Linux (Ubuntu 20.04+), macOS 12+
- **Python**: 3.10 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 2 GB free for models and dependencies
- **Browser**: Chrome 90+, Firefox 90+, Edge 90+ (for frontend UI)
- **Camera**: Optional, for live photo capture

## Installation

### Quick Install (Local)

```bash
# Clone the repository
git clone <repository-url>
cd agriguard-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download model files
# Place disease_model.tflite and phi3.gguf in the models/ directory

# Initialize the database
python -c "from AgriGuard.backend.database import init_db; init_db()"

# Start the application
uvicorn AgriGuard.backend.main:app --host 0.0.0.0 --port 8000
```

### Docker (Recommended for Production)

```bash
# Build the Docker image
docker build -t agriguard-ai:latest .

# Run the container
docker run --rm -p 8000:8000 \
  -v "$(pwd)/models:/app/models" \
  -v "$(pwd)/database:/app/database" \
  agriguard-ai:latest
```

## Configuration

### Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```env
APP_ENV=development
LOG_LEVEL=INFO
MODEL_PATH=models/disease_model.tflite
LLM_MODEL_PATH=models/phi3.gguf
LABELS_PATH=models/labels.txt
DB_PATH=database/agriguard.db
MAX_UPLOAD_SIZE_MB=10
```

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Runtime environment | `development` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `MODEL_PATH` | Path to TFLite classifier | `models/disease_model.tflite` |
| `LLM_MODEL_PATH` | Path to Phi-3 Mini GGUF | `models/phi3.gguf` |
| `LABELS_PATH` | Path to class labels | `models/labels.txt` |
| `DB_PATH` | Path to SQLite database | `database/agriguard.db` |
| `MAX_UPLOAD_SIZE_MB` | Max image size in MB | `10` |

## Running Locally

### Start the Backend

```bash
uvicorn AgriGuard.backend.main:app --reload --port 8000
```

### Start the Frontend (Development Mode)

```bash
cd frontend
npm install
npm run dev
```

### Access the Application

- **Web Interface**: Open `http://localhost:8000` (frontend served by FastAPI)
- **API Documentation**: Open `http://localhost:8000/docs`
- **Frontend Dev Server**: `http://localhost:3000` (if running separately)

## Running with Docker

### Build and Run

```bash
docker build -t agriguard-ai:latest .
docker run --rm -p 8000:8000 \
  -v "$(pwd)/models:/app/models" \
  -v "$(pwd)/database:/app/database" \
  agriguard-ai:latest
```

### Access

- API docs: `http://localhost:8000/docs`
- Web UI: `http://localhost:8000`

## Common Workflows

### Diagnose a Crop Disease

1. Open the application in your browser (http://localhost:8000).
2. Click the camera icon or upload a leaf image (JPEG, PNG, or BMP up to 10 MB).
3. Wait for processing (typically 2–10 seconds depending on hardware).
4. Review the diagnosis results:
   - **Detected Crop**: The identified crop type
   - **Disease**: The diagnosed disease or condition
   - **Confidence**: How confident the model is in its prediction
   - **Severity**: Low, Medium, High, or None
   - **Recommendations**: Actionable treatment steps
   - **Chemical Treatment**: Recommended chemical treatments
   - **Organic Treatment**: Recommended organic treatments
   - **Prevention Tips**: Steps to prevent future outbreaks
5. Save the record to history (automatic) or export as JSON.

### View History

1. Click the **History** tab on the dashboard.
2. Browse through past diagnoses with thumbnails.
3. Filter by:
   - **Crop type** (e.g., Tomato, Potato, Pepper bell)
   - **Severity** (Low, Medium, High)
   - **Date range**
4. Click a record to view full diagnosis details.
5. Delete records individually if needed.

### Export Data

1. Go to **History**.
2. Click **Export JSON** for machine-readable data.
3. Click **Export CSV** for spreadsheet-compatible data.
4. Save the file to your device.

### Offline Usage

After the initial setup, AgriGuard AI works completely offline:
- All model files are stored locally in `models/`.
- The SQLite database stores all records locally in `database/`.
- The frontend is served as a Progressive Web App (PWA).
- No internet connection is needed for any functionality.
- To verify offline operation, disconnect from the internet and test all features.

## API Reference

The backend exposes a RESTful API at `http://localhost:8000`:

### Health Check
```http
GET /health
```
Returns system status including model and database availability.

### Disease Detection
```http
POST /detect
Content-Type: multipart/form-data

file: <image_file>
```
Upload an image for disease detection. Returns:
- `id`: Record ID
- `crop`: Detected crop type
- `disease`: Detected disease
- `confidence`: Prediction confidence (0-1)
- `severity`: Low, Medium, High, or None
- `recommendation`: List of treatment recommendations
- `inference_time_s`: Processing time in seconds

### View History
```http
GET /history?crop=Tomato&severity=High
```
Filter by crop type and/or severity. Returns list of diagnosis records.

### Get Single Record
```http
GET /history/{id}
```
Returns full details of a specific diagnosis.

### Delete Record
```http
DELETE /history/{id}
```
Deletes a diagnosis record and its associated image.

### Export Data
```http
GET /export/csv
GET /export/json
```
Export all records as CSV or JSON.

## Troubleshooting

### Camera Not Working
- Ensure the browser has camera permissions (check browser settings).
- Use HTTPS or localhost for camera access (HTTP may block camera on some browsers).
- On mobile devices, use the file upload option as a fallback.
- Try a different browser (Chrome recommended).

### Slow Inference
- Close other CPU-heavy applications.
- Reduce image resolution before uploading.
- Ensure the TFLite model is quantized (int8/float16) for faster CPU inference.
- Verify llama.cpp is configured to use optimal CPU threads.

### Model Not Found
- Verify `MODEL_PATH` and `LLM_MODEL_PATH` point to existing files.
- Check that model files exist in the `models/` directory.
- Ensure file permissions allow reading the model files.
- Download the required model files if missing.

### Database Errors
- Ensure the `database/` directory exists and is writable.
- Check available disk space.
- If the database is corrupted, delete `agriguard.db` to reset (all data will be lost).
- Verify WAL mode is enabled (automatic).

### Frontend Not Loading
- Ensure the backend server is running on port 8000.
- Clear browser cache and reload.
- Check browser console for JavaScript errors (F12).
- Verify that the frontend files are properly served by the backend.

## FAQ

**Q: Does AgriGuard AI send data to the cloud?**
A: No. All inference, storage, and processing are local. No data leaves the device. This is a core design principle.

**Q: What image formats are supported?**
A: JPEG, PNG, and BMP up to 10 MB. The image is automatically resized to the model's input dimensions.

**Q: Can I use this on a phone without internet?**
A: Yes. If the application is hosted locally on a laptop or packaged as a PWA, it works fully offline on any device with a modern browser.

**Q: How accurate is the disease detection?**
A: The model targets 85%+ top-1 accuracy on the PlantVillage test set. Actual accuracy may vary by crop type, image quality, and lighting conditions.

**Q: What crops and diseases are supported?**
A: The current model supports 38 crop-disease classes from the PlantVillage dataset, including Tomato, Potato, and Pepper bell varieties with diseases like Early blight, Late blight, Bacterial spot, Powdery mildew, and more.

**Q: What if the LLM produces incorrect output?**
A: The system has a curated fallback knowledge base for common diseases. If the LLM output is malformed, the fallback recommendations are used instead.

**Q: Can I add my own crop disease model?**
A: Yes. Replace `models/disease_model.tflite` with your model and update `models/labels.txt` with your class labels. The model must accept 128×128×3 RGB input.

**Q: How do I update the knowledge base?**
A: The knowledge base is in `backend/recommendation.py`. You can add new crop-disease pairs following the existing dictionary format.

## Support

For additional help:
- Open an issue on the GitLab repository
- Contact the development team at team@example.com
- See the [README.md](README.md) for additional documentation
