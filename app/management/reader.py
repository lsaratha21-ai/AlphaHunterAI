"""Document reader for extracting text from PDF and text files."""

from __future__ import annotations

from pathlib import Path

from app.core.exceptions import ProviderError


class DocumentReader:
    """Reader for extracting text from documents."""

    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Read text from a text file.

        Args:
            file_path: Path to the text file.

        Returns:
            Extracted text content.

        Raises:
            ProviderError: If file cannot be read.
        """
        path = Path(file_path)
        if not path.exists():
            raise ProviderError(f"File not found: {file_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ProviderError(f"Failed to read text file: {e}")

    @staticmethod
    def read_pdf_file(file_path: str) -> str:
        """Read text from a PDF file.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text content.

        Raises:
            ProviderError: If file cannot be read or PDF library not available.
        """
        path = Path(file_path)
        if not path.exists():
            raise ProviderError(f"File not found: {file_path}")

        try:
            import pypdf

            text = ""
            with open(path, "rb") as f:
                pdf_reader = pypdf.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            raise ProviderError("pypdf library not installed. Install with: pip install pypdf")
        except Exception as e:
            raise ProviderError(f"Failed to read PDF file: {e}")

    @staticmethod
    def read_document(file_path: str) -> tuple[str, str]:
        """Read a document and detect its type.

        Args:
            file_path: Path to the document.

        Returns:
            Tuple of (document_type, text_content).

        Raises:
            ProviderError: If file cannot be read.
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return "pdf", DocumentReader.read_pdf_file(file_path)
        elif suffix in [".txt", ".md", ".text"]:
            return "text", DocumentReader.read_text_file(file_path)
        else:
            raise ProviderError(f"Unsupported file type: {suffix}")
