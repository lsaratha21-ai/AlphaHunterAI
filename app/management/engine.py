"""Management guidance extraction engine using OpenAI API."""

from __future__ import annotations

from typing import Any

from app.core.exceptions import ProviderError
from app.management.models import GuidanceScore
from app.management.reader import DocumentReader


class GuidanceEngine:
    """Engine for extracting management guidance from documents using OpenAI API."""

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize the Guidance Engine.

        Args:
            api_key: OpenAI API key. If None, reads from environment.
        """
        self.api_key = api_key

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API for text extraction.

        Args:
            prompt: Prompt to send to OpenAI.

        Returns:
            Response from OpenAI.

        Raises:
            ProviderError: If API call fails.
        """
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial analyst expert at extracting management guidance from corporate documents.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content or ""
        except ImportError:
            raise ProviderError("openai library not installed. Install with: pip install openai")
        except Exception as e:
            raise ProviderError(f"OpenAI API call failed: {e}")

    def _extract_guidance_from_text(self, text: str) -> dict[str, Any]:
        """Extract guidance information from document text.

        Args:
            text: Document text content.

        Returns:
            Dictionary with extracted guidance fields.
        """
        prompt = f"""Extract the following information from the document and return as JSON:

Document:
{text[:8000]}

Extract:
1. revenue_outlook: Management's outlook on revenue (positive/neutral/negative)
2. margin_outlook: Management's outlook on profit margins (positive/neutral/negative)
3. demand: Demand trends described (strong/moderate/weak)
4. order_book: Status of order book/backlog (strong/moderate/weak)
5. capex: Capital expenditure plans (increasing/stable/decreasing)
6. expansion: Expansion plans (aggressive/moderate/conservative)
7. risks: List of key risks mentioned
8. management_confidence: Overall confidence level (high/medium/low)
9. overall_sentiment: Overall sentiment (positive/neutral/negative)

Return as JSON with these exact keys. If information is not available, use null."""

        response = self._call_openai(prompt)
        # Parse JSON response
        try:
            import json

            # Extract JSON from response if it contains extra text
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()

            return json.loads(response)
        except Exception as e:
            raise ProviderError(f"Failed to parse OpenAI response: {e}")

    def extract_guidance_from_file(
        self,
        symbol: str,
        file_path: str,
    ) -> GuidanceScore:
        """Extract management guidance from a document file.

        Args:
            symbol: Stock symbol.
            file_path: Path to the document file.

        Returns:
            GuidanceScore with extracted information.

        Raises:
            ProviderError: If extraction fails.
        """
        reader = DocumentReader()
        doc_type, text = reader.read_document(file_path)

        extracted = self._extract_guidance_from_text(text)

        return GuidanceScore(
            symbol=symbol,
            document_type=doc_type,
            revenue_outlook=extracted.get("revenue_outlook"),
            margin_outlook=extracted.get("margin_outlook"),
            demand=extracted.get("demand"),
            order_book=extracted.get("order_book"),
            capex=extracted.get("capex"),
            expansion=extracted.get("expansion"),
            risks=extracted.get("risks"),
            management_confidence=extracted.get("management_confidence"),
            overall_sentiment=extracted.get("overall_sentiment"),
        )

    def extract_guidance_from_text(
        self,
        symbol: str,
        text: str,
        document_type: str = "transcript",
    ) -> GuidanceScore:
        """Extract management guidance from raw text.

        Args:
            symbol: Stock symbol.
            text: Document text content.
            document_type: Type of document (pdf/text/transcript).

        Returns:
            GuidanceScore with extracted information.

        Raises:
            ProviderError: If extraction fails.
        """
        extracted = self._extract_guidance_from_text(text)

        return GuidanceScore(
            symbol=symbol,
            document_type=document_type,
            revenue_outlook=extracted.get("revenue_outlook"),
            margin_outlook=extracted.get("margin_outlook"),
            demand=extracted.get("demand"),
            order_book=extracted.get("order_book"),
            capex=extracted.get("capex"),
            expansion=extracted.get("expansion"),
            risks=extracted.get("risks"),
            management_confidence=extracted.get("management_confidence"),
            overall_sentiment=extracted.get("overall_sentiment"),
        )
