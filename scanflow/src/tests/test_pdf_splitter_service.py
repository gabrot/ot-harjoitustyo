"""PDF-jakamispalvelun yksikkötestit."""
import os
import pytest
import tempfile
import fitz

from src.services.pdf_splitter_service import PDFSplitterService
from src.repositories.pdf_repository import PDFRepository

class TestPDFSplitterService:
    """Testaa PDF-jakamispalvelun toiminnallisuudet."""

    @pytest.fixture
    def splitter_service(self):
        """Luo PDFSplitterService-instanssin testejä varten."""
        return PDFSplitterService()

    @pytest.fixture
    def sample_pdf(self):
        """Luo väliaikainen PDF-tiedosto testausta varten.
        
        Returns:
            str: Väliaikaisen PDF-tiedoston polku
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            doc = fitz.open()
            for _ in range(5):  # Luo 5-sivuinen PDF
                doc.new_page()
            doc.save(temp_file.name)
            doc.close()
            yield temp_file.name
        
        # Poista väliaikainen tiedosto
        os.unlink(temp_file.name)

    def test_get_pdf_info(self, splitter_service, sample_pdf):
        """Testaa PDF-tiedoston tietojen hakeminen."""
        info = splitter_service.get_pdf_info(sample_pdf)
        
        assert 'page_count' in info
        assert 'file_path' in info
        assert 'file_name' in info
        assert info['page_count'] == 5
        assert info['file_path'] == sample_pdf
        assert info['file_name'] == os.path.basename(sample_pdf)

    def test_split_by_fixed_range_success(self, splitter_service, sample_pdf):
        """Testaa PDF:n jakaminen kiinteän sivumäärän mukaan."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_files = splitter_service.split_by_fixed_range(
                sample_pdf, 
                pages_per_file=2, 
                output_dir=temp_dir
            )
            
            assert len(output_files) == 3  # 5 sivua jaetaan 2-2-1 sivuun
            assert all(os.path.exists(f) for f in output_files)
            
            # Varmista sivumäärät
            for pdf in output_files:
                doc = fitz.open(pdf)
                page_count = doc.page_count
                doc.close()
                assert page_count in [2, 2, 1]

    def test_split_by_fixed_range_invalid_pages(self, splitter_service, sample_pdf):
        """Testaa virheellisen sivumäärän käsittely."""
        with pytest.raises(ValueError, match="Sivujen määrän per tiedosto tulee olla vähintään 1"):
            splitter_service.split_by_fixed_range(sample_pdf, pages_per_file=0)

    def test_split_by_custom_ranges_success(self, splitter_service, sample_pdf):
        """Testaa PDF:n jakaminen mukautetuilla sivualueilla."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ranges = [(1, 2), (3, 4), (5, 5)]
            output_files = splitter_service.split_by_custom_ranges(
                sample_pdf, 
                ranges=ranges, 
                output_dir=temp_dir
            )
            
            assert len(output_files) == 3
            assert all(os.path.exists(f) for f in output_files)
            
            # Varmista sivumäärät
            for pdf, (start, end) in zip(output_files, ranges):
                doc = fitz.open(pdf)
                page_count = doc.page_count
                doc.close()
                assert page_count == end - start + 1

    def test_split_by_custom_ranges_empty(self, splitter_service, sample_pdf):
        """Testaa tyhjän sivualueen käsittely."""
        with pytest.raises(ValueError, match="Vähintään yksi sivualue on määritettävä"):
            splitter_service.split_by_custom_ranges(sample_pdf, ranges=[])