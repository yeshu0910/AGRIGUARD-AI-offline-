"""
Detection pipeline — single predict(image_path) → full structured result.
Orchestrates preprocessing → model inference → crop detection → recommendation.
"""

import os
import time
import numpy as np

from preprocess import preprocess
from crop_detector import parse_label
from recommendation import build_report


class DiseaseDetector:
    def __init__(self, model_path: str = "models/disease_model.tflite") -> None:
        self.model_path = model_path
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.model_loaded = False
        self.labels = []
        self.input_size = (128, 128)
        self._load_model()

    def _load_model(self) -> None:
        resolved = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.model_path
        )
        if not os.path.exists(resolved):
            raise FileNotFoundError(
                f"TFLite model not found at {resolved}. "
                "Please place disease_model.tflite in the models/ directory."
            )
        try:
            import tensorflow.lite as tflite
        except ImportError:
            import tflite_runtime.interpreter as tflite
        self.interpreter = tflite.Interpreter(model_path=resolved)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        input_shape = self.input_details[0]["shape"]
        if len(input_shape) == 4:
            _, h, w, _ = input_shape
            self.input_size = (w, h)

        labels_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models", "labels.txt",
        )
        if os.path.exists(labels_path):
            with open(labels_path, "r") as f:
                self.labels = [line.strip() for line in f.readlines() if line.strip()]

        self.model_loaded = True

    def predict(self, image_path: str, extract_leaf: bool = False) -> dict:
        t0 = time.perf_counter()
        input_data = preprocess(image_path, target_size=self.input_size, extract_leaf_region=extract_leaf)
        self.interpreter.set_tensor(self.input_details[0]["index"], input_data)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_details[0]["index"])
        scores = output[0]
        class_index = int(np.argmax(scores))
        confidence = float(scores[class_index])
        raw_label = self.labels[class_index] if class_index < len(self.labels) else "Unknown"
        t1 = time.perf_counter()

        crop, disease = parse_label(raw_label)

        report = build_report(crop, disease)

        return {
            "crop": crop,
            "disease": disease,
            "confidence": round(confidence, 4),
            "class_index": class_index,
            "severity": report["severity"],
            "affected_area": report["affected_area"],
            "recommendation": report["recommendation"],
            "chemical_treatment": report["chemical_treatment"],
            "organic_treatment": report["organic_treatment"],
            "prevention": report["prevention"],
            "inference_time_s": round(t1 - t0, 3),
        }
