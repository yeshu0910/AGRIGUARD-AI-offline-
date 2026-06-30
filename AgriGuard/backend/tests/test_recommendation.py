"""Unit tests for the recommendation engine."""

from recommendation import build_report, get_recommendation


class TestGetRecommendation:
    def test_tomato_early_blight(self):
        result = get_recommendation("Tomato", "Early blight")
        assert result["severity"] == "Medium"
        assert result["affected_area"] == "Lower leaves"
        assert "Mancozeb" in result["chemical"]
        assert len(result["prevention"]) > 0

    def test_tomato_late_blight(self):
        result = get_recommendation("Tomato", "Late blight")
        assert result["severity"] == "High"
        assert "Chlorothalonil" in result["chemical"]
        assert len(result["prevention"]) > 0

    def test_potato_early_blight(self):
        result = get_recommendation("Potato", "Early blight")
        assert result["severity"] == "Medium"
        assert "Mancozeb" in result["chemical"]

    def test_potato_late_blight(self):
        result = get_recommendation("Potato", "Late blight")
        assert result["severity"] == "High"
        assert "Metalaxyl" in result["chemical"]

    def test_healthy_plant(self):
        result = get_recommendation("Tomato", "healthy")
        assert result["severity"] == "None"
        assert "None required" in result["chemical"]

    def test_pepper_bell_bacterial_spot(self):
        result = get_recommendation("Pepper bell", "Bacterial spot")
        assert result["severity"] == "Medium"
        assert "Copper" in result["chemical"]

    def test_unknown_crop(self):
        result = get_recommendation("Unknown", "Unknown disease")
        assert result["severity"] == "Medium"
        assert "extension officer" in result["chemical"].lower()

    def test_case_insensitive_disease(self):
        result = get_recommendation("Tomato", "EARLY BLIGHT")
        assert result["severity"] == "Medium"

    def test_partial_disease_match(self):
        result = get_recommendation("Tomato", "blight")
        assert result["severity"] in ("Medium", "High")


class TestBuildReport:
    def test_build_report_contains_all_keys(self):
        report = build_report("Tomato", "Early blight")
        expected_keys = [
            "severity",
            "affected_area",
            "chemical_treatment",
            "organic_treatment",
            "prevention",
            "recommendation",
        ]
        for key in expected_keys:
            assert key in report, f"Missing key: {key}"

    def test_build_report_recommendations_list(self):
        report = build_report("Tomato", "Early blight")
        assert isinstance(report["recommendation"], list)
        assert len(report["recommendation"]) > 0

    def test_build_report_contains_chemical_and_organic(self):
        report = build_report("Tomato", "Early blight")
        any_chemical = any("[Chemical]" in r for r in report["recommendation"])
        any_organic = any("[Organic]" in r for r in report["recommendation"])
        assert any_chemical
        assert any_organic

    def test_build_report_unknown_disease(self):
        report = build_report("Unknown", "Unknown")
        assert "recommendation" in report
        assert len(report["recommendation"]) > 0

    def test_build_report_prevention_not_empty(self):
        report = build_report("Tomato", "Late blight")
        assert len(report["prevention"]) > 0
