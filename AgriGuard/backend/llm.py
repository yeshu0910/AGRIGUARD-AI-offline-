import json
import os
import time

FALLBACK_REPORTS: dict[str, dict] = {
    "early blight": {
        "severity": "Medium",
        "affected_area": "Lower leaves",
        "recommendation": [
            "Remove infected leaves immediately",
            "Apply Mancozeb fungicide (2g/L water)",
            "Avoid overhead watering",
            "Improve air circulation between plants",
        ],
    },
    "late blight": {
        "severity": "High",
        "affected_area": "Entire plant",
        "recommendation": [
            "Remove and destroy all infected plants",
            "Apply chlorothalonil or copper-based fungicide",
            "Avoid planting in same area for 3 seasons",
            "Ensure proper drainage in the field",
        ],
    },
    "bacterial spot": {
        "severity": "Medium",
        "affected_area": "Leaves and fruit",
        "recommendation": [
            "Apply copper-based bactericide",
            "Avoid working with wet plants",
            "Rotate crops to non-host plants for 2 years",
            "Use disease-free seeds and transplants",
        ],
    },
    "powdery mildew": {
        "severity": "Low",
        "affected_area": "Upper leaf surface",
        "recommendation": [
            "Apply sulfur-based fungicide",
            "Increase spacing between plants",
            "Avoid excess nitrogen fertilization",
            "Use resistant varieties next season",
        ],
    },
    "healthy": {
        "severity": "None",
        "affected_area": "None",
        "recommendation": [
            "Continue current care practices",
            "Monitor plants regularly for early signs",
            "Maintain proper watering and nutrition",
        ],
    },
}


def _find_fallback(disease: str) -> dict | None:
    disease_lower = disease.lower()
    for key, report in FALLBACK_REPORTS.items():
        if key in disease_lower or disease_lower in key:
            return report
    return None


class ReportGenerator:
    def __init__(self, model_path: str | None = None) -> None:
        self.model_path = model_path or os.environ.get("LLM_MODEL_PATH", "models/phi3.gguf")
        self.llm = None
        self._load_model()

    def _load_model(self) -> None:
        resolved = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.model_path
        )
        if not os.path.exists(resolved):
            print(f"[llm] Model not found at {resolved}. Fallback reports will be used.")
            return
        try:
            from llama_cpp import Llama

            self.llm = Llama(
                model_path=resolved,
                n_ctx=2048,
                n_threads=4,
                n_gpu_layers=0,
                verbose=False,
            )
            print("[llm] Local LLM loaded successfully")
        except Exception as e:
            print(f"[llm] Failed to load LLM: {e}. Fallback reports will be used.")

    def generate_report(self, crop: str, disease: str, confidence: float) -> dict:
        if self.llm is None:
            return self.fallback_report(disease)

        prompt = (
            f"You are an agricultural expert AI. A farmer's crop has been analysed. "
            f"Crop: {crop}. Disease: {disease}. Confidence: {confidence}. "
            f"Respond ONLY in valid JSON with keys: severity (Low/Medium/High/None), "
            f"affected_area (string), recommendation (list of 3-5 strings). "
            f"No explanation. JSON only."
        )

        t0 = time.perf_counter()
        try:
            output = self.llm(
                prompt,
                max_tokens=300,
                temperature=0.1,
                stop=None,
            )
            t1 = time.perf_counter()
            print(f"[llm] Report generation completed in {t1 - t0:.3f}s")

            choices = output.get("choices", [])
            if not choices:
                return self.fallback_report(disease)
            raw = choices[0].get("text", "").strip()
            raw = raw.strip().strip("`").strip()
            if raw.startswith("json"):
                raw = raw[4:].strip()
            report = json.loads(raw)
            report.setdefault("severity", "Medium")
            report.setdefault("affected_area", "Unknown")
            report.setdefault("recommendation", ["Monitor closely"])
            return report
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"[llm] JSON parse error: {e}. Using fallback.")
            return self.fallback_report(disease)

    def fallback_report(self, disease: str) -> dict:
        report = _find_fallback(disease)
        if report:
            return report
        return {
            "severity": "Medium",
            "affected_area": "Affected area could not be determined",
            "recommendation": [
                "Consult a local agricultural extension officer",
                "Isolate affected plants to prevent spread",
                "Monitor crop daily for changes",
            ],
        }
