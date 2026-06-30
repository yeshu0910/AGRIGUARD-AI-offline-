"""Integration tests to verify offline-first behavior."""

import importlib.util


class TestOfflineBehavior:
    def _check_no_network(self, module_name: str) -> None:
        spec = importlib.util.find_spec(module_name)
        assert spec is not None, f"Could not find module: {module_name}"
        assert spec.origin is not None, f"No origin for module: {module_name}"
        with open(spec.origin) as f:
            source = f.read()
        forbidden = ["urllib.request", "requests.", "http.client", "socket."]
        for item in forbidden:
            assert item not in source, f"Network call detected in {module_name}: {item}"

    def test_preprocess_no_network(self):
        self._check_no_network("AgriGuard.backend.preprocess")

    def test_crop_detector_no_network(self):
        self._check_no_network("AgriGuard.backend.crop_detector")

    def test_recommendation_no_network(self):
        self._check_no_network("AgriGuard.backend.recommendation")

    def test_detect_no_network(self):
        self._check_no_network("AgriGuard.backend.detect")

    def test_database_no_network(self):
        self._check_no_network("AgriGuard.backend.database")
