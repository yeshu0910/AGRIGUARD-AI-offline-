"""Tests for LLM report generation with mocked Llama."""

from unittest.mock import MagicMock


def test_generate_report_with_mocked_llm():
    """Test that generate_report works with a mocked LLM."""
    from llm import ReportGenerator

    mock_llm = MagicMock()
    mock_llm.return_value = {
        "choices": [
            {
                "text": '{"severity": "High", "affected_area": "Whole plant", "recommendation": ["Remove plant", "Apply fungicide"]}'
            }
        ]
    }

    gen = ReportGenerator.__new__(ReportGenerator)
    gen.llm = mock_llm
    gen.model_path = "fake.gguf"

    result = gen.generate_report("Tomato", "Late blight", 0.95)

    assert result["severity"] == "High"
    assert result["affected_area"] == "Whole plant"
    assert len(result["recommendation"]) == 2
    mock_llm.assert_called_once()


def test_generate_report_malformed_json_falls_back():
    """Test that malformed JSON output falls back gracefully."""
    from llm import ReportGenerator

    mock_llm = MagicMock()
    mock_llm.return_value = {"choices": [{"text": "not valid json at all"}]}

    gen = ReportGenerator.__new__(ReportGenerator)
    gen.llm = mock_llm
    gen.model_path = "fake.gguf"

    result = gen.generate_report("Tomato", "Early blight", 0.85)

    assert "severity" in result
    assert "recommendation" in result
    assert len(result["recommendation"]) > 0


def test_generate_report_empty_choices():
    """Test that empty choices returns fallback."""
    from llm import ReportGenerator

    mock_llm = MagicMock()
    mock_llm.return_value = {"choices": []}

    gen = ReportGenerator.__new__(ReportGenerator)
    gen.llm = mock_llm
    gen.model_path = "fake.gguf"

    result = gen.generate_report("Potato", "Late blight", 0.9)

    assert "severity" in result
    assert "recommendation" in result


def test_generate_report_missing_keys_defaults():
    """Test that missing JSON keys get default values."""
    from llm import ReportGenerator

    mock_llm = MagicMock()
    mock_llm.return_value = {"choices": [{"text": '{"severity": "Low"}'}]}

    gen = ReportGenerator.__new__(ReportGenerator)
    gen.llm = mock_llm
    gen.model_path = "fake.gguf"

    result = gen.generate_report("Tomato", "Early blight", 0.8)

    assert result["severity"] == "Low"
    assert result["affected_area"] == "Unknown"
    assert result["recommendation"] == ["Monitor closely"]


def test_generate_report_json_with_markdown_backticks():
    """Test that JSON wrapped in markdown backticks is parsed correctly."""
    from llm import ReportGenerator

    mock_llm = MagicMock()
    mock_llm.return_value = {
        "choices": [
            {
                "text": '```json\n{"severity": "Medium", "affected_area": "Leaves", "recommendation": ["Spray neem oil"]}\n```'
            }
        ]
    }

    gen = ReportGenerator.__new__(ReportGenerator)
    gen.llm = mock_llm
    gen.model_path = "fake.gguf"

    result = gen.generate_report("Tomato", "Powdery mildew", 0.7)

    assert result["severity"] == "Medium"
    assert result["affected_area"] == "Leaves"
    assert "neem oil" in result["recommendation"][0]
