import csv
import io
import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "agriguard.db"
)


def _get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    conn = _get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS DiseaseLogs (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp       TEXT    NOT NULL,
                crop            TEXT    NOT NULL,
                disease         TEXT    NOT NULL,
                confidence      REAL    NOT NULL,
                severity        TEXT    NOT NULL,
                affected_area   TEXT,
                recommendation  TEXT,
                image_path      TEXT,
                latitude        REAL,
                longitude       REAL
            )
        """)
        conn.commit()
    finally:
        conn.close()


def insert_log(data: dict) -> int:
    conn = _get_connection()
    try:
        data["timestamp"] = data.get("timestamp", datetime.now(timezone.utc).isoformat())
        if isinstance(data.get("recommendation"), list):
            data["recommendation"] = json.dumps(data["recommendation"])

        cursor = conn.execute(
            """
            INSERT INTO DiseaseLogs
                (timestamp, crop, disease, confidence, severity,
                 affected_area, recommendation, image_path, latitude, longitude)
            VALUES
                (:timestamp, :crop, :disease, :confidence, :severity,
                 :affected_area, :recommendation, :image_path, :latitude, :longitude)
        """,
            {
                "timestamp": data["timestamp"],
                "crop": data["crop"],
                "disease": data["disease"],
                "confidence": data["confidence"],
                "severity": data["severity"],
                "affected_area": data.get("affected_area", ""),
                "recommendation": data.get("recommendation", "[]"),
                "image_path": data.get("image_path", ""),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
            },
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    if isinstance(d.get("recommendation"), str):
        try:
            d["recommendation"] = json.loads(d["recommendation"])
        except (json.JSONDecodeError, TypeError):
            d["recommendation"] = []
    return d


def get_all_logs(crop: str | None = None, severity: str | None = None) -> list[dict]:
    conn = _get_connection()
    try:
        query = "SELECT * FROM DiseaseLogs"
        params: list = []
        conditions: list = []
        if crop:
            conditions.append("crop = ?")
            params.append(crop)
        if severity:
            conditions.append("severity = ?")
            params.append(severity)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY id DESC"
        rows = conn.execute(query, params).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def get_log_by_id(log_id: int) -> dict | None:
    conn = _get_connection()
    try:
        row = conn.execute("SELECT * FROM DiseaseLogs WHERE id = ?", (log_id,)).fetchone()
        if row is None:
            return None
        return _row_to_dict(row)
    finally:
        conn.close()


def delete_log(log_id: int) -> bool:
    conn = _get_connection()
    try:
        cursor = conn.execute("DELETE FROM DiseaseLogs WHERE id = ?", (log_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def export_all_as_csv() -> str:
    conn = _get_connection()
    try:
        cursor = conn.execute("SELECT * FROM DiseaseLogs ORDER BY id DESC")
        rows = cursor.fetchall()
        if not rows:
            return ""
        col_names = [desc[0] for desc in cursor.description]
        rec_index = col_names.index("recommendation") if "recommendation" in col_names else -1
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(col_names)
        for row in rows:
            cleaned = []
            for i, v in enumerate(row):
                if (i == rec_index and isinstance(v, str)) or isinstance(v, str):
                    cleaned.append(v)
                elif v is None:
                    cleaned.append("")
                else:
                    cleaned.append(str(v))
            writer.writerow(cleaned)
        return output.getvalue()
    finally:
        conn.close()
