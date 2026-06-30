"""Unit tests for the FastAPI application endpoints."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _mock_detector():
    det = MagicMock()
    det.predict.return_value = {
        "crop": "Tomato",
        "disease": "Early blight",
        "confidence": 0.95,
        "class_index": 1,
        "severity": "Medium",
        "affected_area": "Lower leaves",
        "recommendation": ["Remove leaves", "Apply fungicide"],
        "chemical_treatment": "Chlorothalonil",
        "organic_treatment": "Neem oil",
        "prevention": "Rotate crops",
        "inference_time_s": 0.5,
    }
    return det


def _mock_reporter():
    rep = MagicMock()
    rep.generate_report.return_value = {
        "severity": "Medium",
        "affected_area": "Lower leaves",
        "recommendation": ["Step 1", "Step 2"],
    }
    return rep


@pytest.fixture
def client():
    with (
        patch("app.init_db"),
        patch("app.insert_log", return_value=1),
        patch("app.get_all_logs", return_value=[]),
        patch("app.get_log_by_id", return_value=None),
        patch("app.delete_log", return_value=True),
        patch("app.export_all_as_csv", return_value="crop,disease\nTomato,Early blight"),
        patch("app.get_detector", return_value=_mock_detector()),
        patch("app.get_reporter", return_value=_mock_reporter()),
        patch("app.os.path.exists", return_value=True),
        patch("app.os.makedirs"),
        patch("app.shutil.disk_usage", return_value=(100, 50, 50)),
    ):
        from app import app

        with TestClient(app) as c:
            yield c


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "model_loaded" in data
        assert "llm_available" in data
        assert "database_initialized" in data
        assert "disk_space_mb" in data


class TestDetectEndpoint:
    def test_detect_without_file_returns_422(self, client):
        response = client.post("/detect")
        assert response.status_code == 422

    def test_detect_with_valid_image(self, client):
        response = client.post(
            "/detect",
            files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["crop"] == "Tomato"
        assert data["disease"] == "Early blight"
        assert data["confidence"] == 0.95
        assert "id" in data
        assert "recommendation" in data

    def test_detect_model_not_found(self, client):
        error_det = MagicMock()
        error_det.predict.side_effect = FileNotFoundError("Model not found")

        with patch("app.get_detector", return_value=error_det):
            response = client.post(
                "/detect",
                files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
            )
            assert response.status_code == 503

    def test_detect_general_error(self, client):
        error_det = MagicMock()
        error_det.predict.side_effect = ValueError("Something went wrong")

        with patch("app.get_detector", return_value=error_det):
            response = client.post(
                "/detect",
                files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
            )
            assert response.status_code == 500
            assert "Detection failed" in response.json()["detail"]

    def test_detect_llm_fallback(self, client):
        error_rep = MagicMock()
        error_rep.generate_report.side_effect = Exception("LLM error")

        with patch("app.get_reporter", return_value=error_rep):
            response = client.post(
                "/detect",
                files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
            )
            assert response.status_code == 200
            data = response.json()
            assert "Remove leaves" in data["recommendation"]


class TestHistoryEndpoint:
    def test_history_empty(self, client):
        response = client.get("/history")
        assert response.status_code == 200
        assert response.json() == []

    def test_history_with_logs(self, client):
        logs = [
            {
                "id": 1,
                "crop": "Tomato",
                "disease": "Early blight",
                "confidence": 0.95,
                "severity": "Medium",
                "affected_area": "Leaves",
                "recommendation": ["Remove"],
                "image_path": "images/test.jpg",
                "timestamp": "2024-01-01T00:00:00",
            }
        ]
        with patch("app.get_all_logs", return_value=logs):
            response = client.get("/history")
            assert response.status_code == 200
            assert len(response.json()) == 1
            assert response.json()[0]["crop"] == "Tomato"

    def test_history_detail_found(self, client):
        log = {
            "id": 1,
            "crop": "Tomato",
            "disease": "Early blight",
            "confidence": 0.95,
            "severity": "Medium",
            "affected_area": "Leaves",
            "recommendation": ["Remove"],
            "image_path": "images/test.jpg",
            "timestamp": "2024-01-01T00:00:00",
        }
        with patch("app.get_log_by_id", return_value=log):
            response = client.get("/history/1")
            assert response.status_code == 200
            assert response.json()["crop"] == "Tomato"

    def test_history_detail_not_found(self, client):
        response = client.get("/history/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Log entry not found"

    def test_history_delete_found(self, client):
        log = {
            "id": 1,
            "crop": "Tomato",
            "disease": "Early blight",
            "image_path": "images/test.jpg",
        }
        with (
            patch("app.get_log_by_id", return_value=log),
            patch("app.os.path.exists", return_value=False),
        ):
            response = client.delete("/history/1")
            assert response.status_code == 200
            assert response.json()["detail"] == "Log entry deleted"

    def test_history_delete_not_found(self, client):
        response = client.delete("/history/999")
        assert response.status_code == 404


class TestExportEndpoints:
    def test_export_csv(self, client):
        response = client.get("/export/csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers["content-type"]
        assert "Tomato" in response.text

    def test_export_json(self, client):
        with patch("app.get_all_logs", return_value=[{"crop": "Tomato"}]):
            response = client.get("/export/json")
            assert response.status_code == 200
            assert "application/json" in response.headers["content-type"]
            assert "Tomato" in response.text


class TestFrontendServing:
    def test_root_serves_index(self, client):
        with patch("app.os.path.isfile", return_value=False):
            response = client.get("/")
            assert response.status_code == 200

    def test_static_file_served(self, client, tmp_path):
        css_file = tmp_path / "style.css"
        css_file.write_text("body { color: red; }")

        with (
            patch("app.FRONTEND_DIR", str(tmp_path)),
            patch("app.os.path.isfile", return_value=True),
        ):
            response = client.get("/style.css")
            assert response.status_code == 200
