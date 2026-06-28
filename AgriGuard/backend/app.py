import json
import os
import sys
import uuid
import shutil
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import init_db, insert_log, get_all_logs, get_log_by_id, delete_log, export_all_as_csv
from detect import DiseaseDetector
from llm import ReportGenerator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
os.makedirs(IMAGES_DIR, exist_ok=True)

app = FastAPI(title="AgriGuard AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

detector: Optional[DiseaseDetector] = None
reporter: Optional[ReportGenerator] = None


def get_detector() -> DiseaseDetector:
    global detector
    if detector is None:
        detector = DiseaseDetector(
            model_path=os.path.join("models", "disease_model.tflite")
        )
    return detector


def get_reporter() -> ReportGenerator:
    global reporter
    if reporter is None:
        reporter = ReportGenerator(
            model_path=os.path.join("models", "phi3.gguf")
        )
    return reporter


@app.on_event("startup")
async def startup() -> None:
    init_db()


@app.get("/health")
async def health() -> dict:
    model_ok = False
    model_path = os.path.join(BASE_DIR, "models", "disease_model.tflite")
    if os.path.exists(model_path):
        try:
            get_detector()
            model_ok = True
        except Exception:
            model_ok = False

    llm_path = os.path.join(BASE_DIR, "models", "phi3.gguf")
    llm_ok = os.path.exists(llm_path)

    db_ok = os.path.exists(os.path.join(BASE_DIR, "database", "agriguard.db"))

    total, used, free = shutil.disk_usage(BASE_DIR)

    return {
        "status": "ok",
        "model_loaded": model_ok,
        "llm_available": llm_ok,
        "database_initialized": db_ok,
        "disk_space_mb": round(free / (1024 * 1024), 1),
    }


@app.post("/detect")
async def detect(file: UploadFile = File(...)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    image_path = os.path.join(IMAGES_DIR, filename)

    content = await file.read()
    with open(image_path, "wb") as f:
        f.write(content)

    try:
        det = get_detector()
        result = det.predict(image_path, extract_leaf=False)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)
        raise HTTPException(status_code=500, detail=f"Detection failed: {e}")

    try:
        rep = get_reporter()
        llm_report = rep.generate_report(result["crop"], result["disease"], result["confidence"])
        llm_recs = llm_report.get("recommendation", [])
        report = result["recommendation"] + ["---"] + llm_recs
    except Exception:
        report = result["recommendation"]

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "crop": result["crop"],
        "disease": result["disease"],
        "confidence": result["confidence"],
        "severity": result["severity"],
        "affected_area": result["affected_area"],
        "recommendation": json.dumps(report),
        "image_path": os.path.join("images", filename),
    }

    log_id = insert_log(log_data)

    return {
        "id": log_id,
        "timestamp": log_data["timestamp"],
        "crop": result["crop"],
        "disease": result["disease"],
        "confidence": result["confidence"],
        "severity": result["severity"],
        "affected_area": result["affected_area"],
        "recommendation": report,
        "chemical_treatment": result["chemical_treatment"],
        "organic_treatment": result["organic_treatment"],
        "prevention": result["prevention"],
        "inference_time_s": result["inference_time_s"],
        "image_path": log_data["image_path"],
    }


@app.get("/history")
async def history(crop: Optional[str] = Query(None), severity: Optional[str] = Query(None)) -> list[dict]:
    return get_all_logs(crop=crop, severity=severity)


@app.get("/history/{log_id}")
async def history_detail(log_id: int) -> dict:
    log = get_log_by_id(log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return log


@app.delete("/history/{log_id}")
async def history_delete(log_id: int) -> dict:
    log = get_log_by_id(log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Log entry not found")

    image_path = log.get("image_path", "")
    if image_path:
        full_path = os.path.join(BASE_DIR, image_path)
        if os.path.exists(full_path):
            os.remove(full_path)

    delete_log(log_id)
    return {"detail": "Log entry deleted"}


@app.get("/export/csv")
async def export_csv() -> Response:
    csv_content = export_all_as_csv()
    filename = f"agriguard_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/export/json")
async def export_json() -> Response:
    logs = get_all_logs()
    filename = f"agriguard_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    return Response(
        content=json.dumps(logs, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/{path:path}")
async def serve_frontend(path: str) -> FileResponse:
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
