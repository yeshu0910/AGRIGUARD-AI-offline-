"""Unit tests for the LLM report generator."""

import pytest

from llm import FALLBACK_REPORTS, ReportGenerator, _find_fallback


class TestFallbackReports:
    def test_find_fallback_early_blight(self):
        report = _find_fallback("Early blight")
        assert report is not None
        assert report["severity"] == "Medium"
        assert "Mancozeb" in report["recommendation"][1]

    def test_find_fallback_late_blight(self):
        report = _find_fallback("Late blight")
        assert report is not None
        assert report["severity"] == "High"
        assert "destroy" in report["recommendation"][0].lower()

    def test_find_fallback_bacterial_spot(self):
        report = _find_fallback("Bacterial spot")
        assert report is not None
        assert "copper" in report["recommendation"][0].lower()

    def test_find_fallback_powdery_mildew(self):
        report = _find_fallback("Powdery mildew")
        assert report is not None
        assert report["severity"] == "Low"

    def test_find_fallback_healthy(self):
        report = _find_fallback("healthy")
        assert report is not None
        assert report["severity"] == "None"

    def test_find_fallback_unknown(self):
        report = _find_fallback("Some unknown disease")
        assert report is None

    def test_find_fallback_partial_match(self):
        report = _find_fallback("early blight on tomato")
        assert report is not None
        assert report["severity"] == "Medium"


class TestReportGeneratorInit:
    def test_init_model_not_found(self):
        gen = ReportGenerator(model_path="nonexistent.gguf")
        assert gen.llm is None

    def test_init_uses_fallback_when_llm_unavailable(self):
        gen = ReportGenerator(model_path="nonexistent.gguf")
        assert gen.llm is None
        report = gen.generate_report("Tomato", "Early blight", 0.85)
        assert report["severity"] == "Medium"
        assert "recommendation" in report


class TestReportGeneratorFallback:
    @pytest.fixture
    def fallback_gen(self):
        return ReportGenerator(model_path="nonexistent.gguf")

    def test_fallback_for_known_disease(self, fallback_gen):
        report = fallback_gen.generate_report("Tomato", "Early blight", 0.95)
        assert report["severity"] == "Medium"
        assert len(report["recommendation"]) > 0

    def test_fallback_for_unknown_disease(self, fallback_gen):
        report = fallback_gen.generate_report("Unknown", "Unknown disease", 0.5)
        assert "recommendation" in report
        assert len(report["recommendation"]) > 0

    def test_fallback_for_healthy(self, fallback_gen):
        report = fallback_gen.generate_report("Tomato", "healthy", 0.99)
        assert report["severity"] == "None"
        assert "Continue" in report["recommendation"][0]

    def test_fallback_structure(self, fallback_gen):
        report = fallback_gen.generate_report("Potato", "Late blight", 0.9)
        expected_keys = ["severity", "affected_area", "recommendation"]
        for key in expected_keys:
            assert key in report
        assert isinstance(report["recommendation"], list)


class TestFALLBACK_REPORTS:
    def test_all_fallbacks_have_required_keys(self):
        required = ["severity", "affected_area", "recommendation"]
        for disease, report in FALLBACK_REPORTS.items():
            for key in required:
                assert key in report

    def test_all_recommendations_are_lists(self):
        for disease, report in FALLBACK_REPORTS.items():
            assert isinstance(report["recommendation"], list)

    def test_all_recommendations_non_empty(self):
        for disease, report in FALLBACK_REPORTS.items():
            assert len(report["recommendation"]) > 0

    def test_severity_values_valid(self):
        valid = {"Low", "Medium", "High", "None"}
        for disease, report in FALLBACK_REPORTS.items():
            assert report["severity"] in valid
