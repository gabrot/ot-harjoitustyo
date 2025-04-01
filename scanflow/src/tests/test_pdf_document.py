"""PDF-dokumentin yksikkötestit."""
import pytest
import os
from src.entities.pdf_document import PDFDocument

class TestPDFDocument:
    """Testaa PDF-dokumentin toiminnallisuudet."""

    def test_pdf_document_creation(self):
        """Testaa PDF-dokumentin luominen."""
        test_path = "/path/to/test.pdf"
        test_page_count = 5

        # Luo PDF-dokumentti
        pdf_doc = PDFDocument(test_path, test_page_count)

        # Varmista attribuuttien oikeellisuus
        assert pdf_doc.file_path == test_path
        assert pdf_doc.page_count == test_page_count