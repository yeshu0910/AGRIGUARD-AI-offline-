"""Unit tests for the database module."""

import os
import tempfile
from unittest.mock import patch

import pytest


@pytest.fixture
def db_path():
    """Create a temporary database path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = os.path.join(tmpdir, "test_agriguard.db")
        with patch("database.DB_PATH", db_file):
            yield db_file


class TestDatabaseInit:
    def test_init_db_creates_table(self, db_path):
        from database import _get_connection, init_db

        init_db()
        conn = _get_connection()
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='DiseaseLogs'"
            )
            assert cursor.fetchone() is not None
        finally:
            conn.close()

    def test_init_db_idempotent(self, db_path):
        from database import init_db

        init_db()
        init_db()
        init_db()


class TestInsertAndRetrieve:
    def test_insert_and_get_log(self, db_path):
        from database import get_log_by_id, init_db, insert_log

        init_db()

        data = {
            "crop": "Tomato",
            "disease": "Early blight",
            "confidence": 0.95,
            "severity": "Medium",
            "affected_area": "Lower leaves",
            "recommendation": ["Remove leaves", "Apply fungicide"],
            "image_path": "images/test.jpg",
        }
        log_id = insert_log(data)
        assert log_id > 0

        result = get_log_by_id(log_id)
        assert result is not None
        assert result["crop"] == "Tomato"
        assert result["disease"] == "Early blight"
        assert result["confidence"] == 0.95
        assert result["severity"] == "Medium"

    def test_get_all_logs(self, db_path):
        from database import get_all_logs, init_db, insert_log

        init_db()

        insert_log(
            {
                "crop": "Tomato",
                "disease": "Early blight",
                "confidence": 0.9,
                "severity": "Medium",
            }
        )
        insert_log(
            {
                "crop": "Potato",
                "disease": "Late blight",
                "confidence": 0.85,
                "severity": "High",
            }
        )

        logs = get_all_logs()
        assert len(logs) == 2

    def test_get_logs_filter_by_crop(self, db_path):
        from database import get_all_logs, init_db, insert_log

        init_db()

        insert_log(
            {"crop": "Tomato", "disease": "Early blight", "confidence": 0.9, "severity": "Medium"}
        )
        insert_log(
            {"crop": "Potato", "disease": "Late blight", "confidence": 0.85, "severity": "High"}
        )

        tomato_logs = get_all_logs(crop="Tomato")
        assert len(tomato_logs) == 1
        assert tomato_logs[0]["crop"] == "Tomato"

    def test_get_logs_filter_by_severity(self, db_path):
        from database import get_all_logs, init_db, insert_log

        init_db()

        insert_log(
            {"crop": "Tomato", "disease": "Early blight", "confidence": 0.9, "severity": "Medium"}
        )
        insert_log(
            {"crop": "Potato", "disease": "Late blight", "confidence": 0.85, "severity": "High"}
        )

        high_logs = get_all_logs(severity="High")
        assert len(high_logs) == 1
        assert high_logs[0]["severity"] == "High"

    def test_get_log_by_id_not_found(self, db_path):
        from database import get_log_by_id, init_db

        init_db()
        result = get_log_by_id(999)
        assert result is None

    def test_get_log_with_invalid_json_recommendation(self, db_path):
        from database import _get_connection, get_all_logs, init_db, insert_log

        init_db()

        log_id = insert_log(
            {
                "crop": "Tomato",
                "disease": "Early blight",
                "confidence": 0.9,
                "severity": "Medium",
                "recommendation": "not-valid-json",
            }
        )
        assert log_id > 0

        logs = get_all_logs()
        assert len(logs) == 1
        assert logs[0]["recommendation"] == []

        conn = _get_connection()
        try:
            conn.execute(
                "UPDATE DiseaseLogs SET recommendation = ? WHERE id = ?",
                ("{malformed json", log_id),
            )
            conn.commit()
        finally:
            conn.close()

        logs = get_all_logs()
        assert logs[0]["recommendation"] == []


class TestDeleteLog:
    def test_delete_existing_log(self, db_path):
        from database import delete_log, get_log_by_id, init_db, insert_log

        init_db()

        log_id = insert_log(
            {"crop": "Tomato", "disease": "Early blight", "confidence": 0.9, "severity": "Medium"}
        )
        result = delete_log(log_id)
        assert result is True
        assert get_log_by_id(log_id) is None

    def test_delete_nonexistent_log(self, db_path):
        from database import delete_log, init_db

        init_db()
        result = delete_log(999)
        assert result is False


class TestExportCSV:
    def test_export_csv_empty(self, db_path):
        from database import export_all_as_csv, init_db

        init_db()
        csv_content = export_all_as_csv()
        assert csv_content == ""

    def test_export_csv_with_data(self, db_path):
        from database import export_all_as_csv, init_db, insert_log

        init_db()

        insert_log(
            {"crop": "Tomato", "disease": "Early blight", "confidence": 0.9, "severity": "Medium"}
        )
        insert_log(
            {"crop": "Potato", "disease": "Late blight", "confidence": 0.85, "severity": "High"}
        )

        csv_content = export_all_as_csv()
        assert "Tomato" in csv_content
        assert "Potato" in csv_content
        assert "Early blight" in csv_content
        assert "Late blight" in csv_content
