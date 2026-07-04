"""Unit tests for the Management Guidance Engine."""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from app.core import ProviderError
from app.management import DocumentReader, GuidanceEngine, GuidanceScore


class TestGuidanceScore:
    """Tests for GuidanceScore model."""

    def test_guidance_score_to_dict(self) -> None:
        """Ensure GuidanceScore converts to dictionary correctly."""
        score = GuidanceScore(
            symbol="AAPL",
            document_type="pdf",
            revenue_outlook="positive",
            margin_outlook="positive",
            demand="strong",
            order_book="strong",
            capex="increasing",
            expansion="aggressive",
            risks=["competition", "regulation"],
            management_confidence="high",
            overall_sentiment="positive",
        )
        result = score.to_dict()
        assert result["symbol"] == "AAPL"
        assert result["revenue_outlook"] == "positive"
        assert result["risks"] == ["competition", "regulation"]


class TestDocumentReader:
    """Tests for DocumentReader."""

    def test_read_text_file_success(self, tmp_path: MockerFixture) -> None:
        """Test reading a text file successfully."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("Sample document content")
        result = DocumentReader.read_text_file(str(text_file))
        assert result == "Sample document content"

    def test_read_text_file_not_found(self) -> None:
        """Test reading a non-existent text file."""
        with pytest.raises(ProviderError, match="File not found"):
            DocumentReader.read_text_file("nonexistent.txt")

    def test_read_document_unsupported_type(self, tmp_path: MockerFixture) -> None:
        """Test reading an unsupported file type."""
        doc_file = tmp_path / "test.doc"
        doc_file.write_text("content")
        with pytest.raises(ProviderError, match="Unsupported file type"):
            DocumentReader.read_document(str(doc_file))

    def test_read_document_text(self, tmp_path: MockerFixture) -> None:
        """Test reading a text document."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("Sample content")
        doc_type, content = DocumentReader.read_document(str(text_file))
        assert doc_type == "text"
        assert content == "Sample content"

    def test_read_document_not_found(self) -> None:
        """Test reading a non-existent document."""
        with pytest.raises(ProviderError, match="File not found"):
            DocumentReader.read_document("nonexistent.pdf")


class TestGuidanceEngine:
    """Tests for GuidanceEngine."""

    def test_guidance_engine_init(self) -> None:
        """Test GuidanceEngine initialization."""
        engine = GuidanceEngine(api_key="test_key")
        assert engine.api_key == "test_key"

    def test_guidance_engine_init_no_key(self) -> None:
        """Test GuidanceEngine initialization without API key."""
        engine = GuidanceEngine()
        assert engine.api_key is None

    def test_extract_guidance_from_text_missing_openai(self, mocker: MockerFixture) -> None:
        """Test extraction when OpenAI library is not installed."""
        mocker.patch.dict("sys.modules", {"openai": None})
        engine = GuidanceEngine(api_key="test_key")
        with pytest.raises(ProviderError, match="openai library not installed"):
            engine.extract_guidance_from_text("AAPL", "sample text")

    def test_extract_guidance_from_file_missing_openai(self, mocker: MockerFixture, tmp_path: MockerFixture) -> None:
        """Test file extraction when OpenAI library is not installed."""
        mocker.patch.dict("sys.modules", {"openai": None})
        engine = GuidanceEngine(api_key="test_key")
        text_file = tmp_path / "test.txt"
        text_file.write_text("Sample content")
        with pytest.raises(ProviderError, match="openai library not installed"):
            engine.extract_guidance_from_file("AAPL", str(text_file))

    def test_extract_guidance_from_text_api_error(self, mocker: MockerFixture) -> None:
        """Test extraction when OpenAI API call fails."""
        mock_openai = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.choices = [mocker.MagicMock(message=mocker.MagicMock(content=None))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.OpenAI.return_value = mock_client
        mocker.patch.dict("sys.modules", {"openai": mock_openai})

        engine = GuidanceEngine(api_key="test_key")
        with pytest.raises(ProviderError, match="Failed to parse OpenAI response"):
            engine.extract_guidance_from_text("AAPL", "sample text")

    def test_extract_guidance_from_text_json_parse_error(self, mocker: MockerFixture) -> None:
        """Test extraction when JSON parsing fails."""
        mock_openai = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.choices = [mocker.MagicMock(message=mocker.MagicMock(content="invalid json"))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.OpenAI.return_value = mock_client
        mocker.patch.dict("sys.modules", {"openai": mock_openai})

        engine = GuidanceEngine(api_key="test_key")
        with pytest.raises(ProviderError, match="Failed to parse OpenAI response"):
            engine.extract_guidance_from_text("AAPL", "sample text")

    def test_extract_guidance_from_text_success(self, mocker: MockerFixture) -> None:
        """Test successful guidance extraction from text."""
        mock_openai = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.choices = [
            mocker.MagicMock(
                message=mocker.MagicMock(
                    content='{"revenue_outlook": "positive", "margin_outlook": "positive", "demand": "strong", "order_book": "strong", "capex": "increasing", "expansion": "aggressive", "risks": ["competition"], "management_confidence": "high", "overall_sentiment": "positive"}'
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.OpenAI.return_value = mock_client
        mocker.patch.dict("sys.modules", {"openai": mock_openai})

        engine = GuidanceEngine(api_key="test_key")
        result = engine.extract_guidance_from_text("AAPL", "sample text")
        assert isinstance(result, GuidanceScore)
        assert result.symbol == "AAPL"
        assert result.revenue_outlook == "positive"
        assert result.risks == ["competition"]

    def test_extract_guidance_from_text_with_json_block(self, mocker: MockerFixture) -> None:
        """Test extraction when response contains JSON code block."""
        mock_openai = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.choices = [
            mocker.MagicMock(
                message=mocker.MagicMock(
                    content='Here is the extracted information:\n```json\n{"revenue_outlook": "positive", "margin_outlook": "neutral", "demand": "moderate", "order_book": "moderate", "capex": "stable", "expansion": "moderate", "risks": [], "management_confidence": "medium", "overall_sentiment": "neutral"}\n```'
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.OpenAI.return_value = mock_client
        mocker.patch.dict("sys.modules", {"openai": mock_openai})

        engine = GuidanceEngine(api_key="test_key")
        result = engine.extract_guidance_from_text("AAPL", "sample text")
        assert isinstance(result, GuidanceScore)
        assert result.revenue_outlook == "positive"
        assert result.overall_sentiment == "neutral"

    def test_extract_guidance_from_file_success(self, mocker: MockerFixture, tmp_path: MockerFixture) -> None:
        """Test successful guidance extraction from file."""
        mock_openai = mocker.MagicMock()
        mock_client = mocker.MagicMock()
        mock_response = mocker.MagicMock()
        mock_response.choices = [
            mocker.MagicMock(
                message=mocker.MagicMock(
                    content='{"revenue_outlook": "positive", "margin_outlook": "positive", "demand": "strong", "order_book": "strong", "capex": "increasing", "expansion": "aggressive", "risks": [], "management_confidence": "high", "overall_sentiment": "positive"}'
                )
            )
        ]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.OpenAI.return_value = mock_client
        mocker.patch.dict("sys.modules", {"openai": mock_openai})

        engine = GuidanceEngine(api_key="test_key")
        text_file = tmp_path / "test.txt"
        text_file.write_text("Sample document content")
        result = engine.extract_guidance_from_file("AAPL", str(text_file))
        assert isinstance(result, GuidanceScore)
        assert result.symbol == "AAPL"
        assert result.document_type == "text"
