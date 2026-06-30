"""Unit tests for crop disease label parser."""

from crop_detector import parse_label


class TestParseLabel:
    def test_tomato_healthy(self):
        crop, disease = parse_label("Tomato___healthy")
        assert crop == "Tomato"
        assert disease == "healthy"

    def test_tomato_bacterial_spot(self):
        crop, disease = parse_label("Tomato___Bacterial_spot")
        assert crop == "Tomato"
        assert disease == "Bacterial spot"

    def test_tomato_early_blight(self):
        crop, disease = parse_label("Tomato___Early_blight")
        assert crop == "Tomato"
        assert disease == "Early blight"

    def test_tomato_late_blight(self):
        crop, disease = parse_label("Tomato___Late_blight")
        assert crop == "Tomato"
        assert disease == "Late blight"

    def test_pepper_bell_bacterial_spot(self):
        crop, disease = parse_label("Pepper___bell_Bacterial_spot")
        assert crop == "Pepper bell"
        assert disease == "Bacterial spot"

    def test_pepper_bell_healthy(self):
        crop, disease = parse_label("Pepper___bell_healthy")
        assert crop == "Pepper bell"
        assert disease == "healthy"

    def test_potato_early_blight(self):
        crop, disease = parse_label("Potato___Early_blight")
        assert crop == "Potato"
        assert disease == "Early blight"

    def test_potato_late_blight(self):
        crop, disease = parse_label("Potato___Late_blight")
        assert crop == "Potato"
        assert disease == "Late blight"

    def test_potato_healthy(self):
        crop, disease = parse_label("Potato___healthy")
        assert crop == "Potato"
        assert disease == "healthy"

    def test_unknown_format_defaults_to_healthy(self):
        crop, disease = parse_label("UnknownLabel")
        assert crop == "UnknownLabel"
        assert disease == "healthy"

    def test_multi_word_disease(self):
        crop, disease = parse_label("Tomato___Tomato_YellowLeaf_Curl_Virus")
        assert crop == "Tomato"
        assert "Yellow Leaf" in disease or "YellowLeaf" in disease

    def test_empty_label_defaults_to_healthy(self):
        crop, disease = parse_label("")
        assert crop == ""
        assert disease == "healthy"

    def test_no_disease_part_defaults_to_healthy(self):
        crop, disease = parse_label("Corn")
        assert crop == "Corn"
        assert disease == "healthy"
