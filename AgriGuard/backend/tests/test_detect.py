"""Unit tests for the disease detection pipeline."""

import os
from unittest.mock import MagicMock

import numpy as np
import pytest

from detect import DiseaseDetector


class TestDiseaseDetectorInit:
    def test_init_model_not_found(self):
        with pytest.raises(FileNotFoundError, match="TFLite model not found"):
            DiseaseDetector(model_path="nonexistent_model.tflite")


class TestDiseaseDetectorPredict:
    @pytest.fixture
    def mock_detector(self):
        detector = DiseaseDetector.__new__(DiseaseDetector)
        detector.model_path = "models/disease_model.tflite"
        detector.model_loaded = True
        detector.labels = [
            "Tomato___healthy",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Bacterial_spot",
            "Potato___Early_blight",
            "Potato___Late_blight",
        ]
        detector.input_size = (128, 128)
        detector.interpreter = MagicMock()
        detector.input_details = [{"index": 0, "shape": [1, 128, 128, 3]}]
        detector.output_details = [{"index": 1, "shape": [1, 6]}]
        return detector

    def _create_test_image(self, tmp_path, name="test.jpg") -> str:
        import cv2

        img = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
        path = os.path.join(tmp_path, name)
        cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        return path

    def test_predict_returns_expected_keys(self, mock_detector, tmp_path):
        mock_detector.interpreter.get_tensor.return_value = np.array(
            [[0.1, 0.7, 0.1, 0.05, 0.03, 0.02]], dtype=np.float32
        )
        result = mock_detector.predict(self._create_test_image(tmp_path))
        expected_keys = [
            "crop",
            "disease",
            "confidence",
            "class_index",
            "severity",
            "affected_area",
            "recommendation",
            "chemical_treatment",
            "organic_treatment",
            "prevention",
            "inference_time_s",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_predict_returns_high_confidence_for_dominant_class(self, mock_detector, tmp_path):
        mock_detector.interpreter.get_tensor.return_value = np.array(
            [[0.01, 0.95, 0.01, 0.01, 0.01, 0.01]], dtype=np.float32
        )
        result = mock_detector.predict(self._create_test_image(tmp_path))
        assert result["confidence"] > 0.9
        assert result["disease"] in ["Early blight", "Late blight", "healthy", "Bacterial spot"]

    def test_predict_handles_single_class(self, mock_detector, tmp_path):
        mock_detector.interpreter.get_tensor.return_value = np.array(
            [[0.8, 0.05, 0.05, 0.05, 0.03, 0.02]], dtype=np.float32
        )
        result = mock_detector.predict(self._create_test_image(tmp_path))
        assert 0 <= result["confidence"] <= 1.0

    def test_predict_inference_time_positive(self, mock_detector, tmp_path):
        mock_detector.interpreter.get_tensor.return_value = np.array(
            [[0.1, 0.7, 0.1, 0.05, 0.03, 0.02]], dtype=np.float32
        )
        result = mock_detector.predict(self._create_test_image(tmp_path))
        assert result["inference_time_s"] > 0
        assert isinstance(result["inference_time_s"], float)

    def test_predict_confidence_distribution(self, mock_detector, tmp_path):
        num_classes = len(mock_detector.labels)
        scores = np.random.dirichlet(np.ones(num_classes), size=1).astype(np.float32)
        mock_detector.interpreter.get_tensor.return_value = scores
        result = mock_detector.predict(self._create_test_image(tmp_path))
        assert 0 <= result["confidence"] <= 1.0
