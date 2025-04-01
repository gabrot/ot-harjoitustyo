"""PDF-repositorion yksikkötestit."""
import os
import pytest
import tempfile
import fitz

from src.repositories.pdf_repository import PDFRepository

class TestPDFRepository:
    """Testaa PDF-repositorion toiminnallisuudet."""

    @pytest.fixture
    def pdf_repository(self):
        """Luo PDFRepository-instanssin testejä varten."""
        return PDFRepository()

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

    def test_load_pdf_success(self, pdf_repository, sample_pdf):
        """Testaa PDF-tiedoston lataaminen onnistuneesti."""
        pdf_doc = pdf_repository.load_pdf(sample_pdf)
        
        assert pdf_doc is not None
        assert isinstance(pdf_doc, fitz.Document)
        
        # Sulje dokumentti
        pdf_doc.close()

    def test_load_pdf_file_not_found(self, pdf_repository):
        """Testaa virheellisen tiedostopolun käsittely."""
        with pytest.raises(FileNotFoundError):
            pdf_repository.load_pdf("/path/to/nonexistent/file.pdf")

    def test_get_page_count(self, pdf_repository, sample_pdf):
        """Testaa PDF-dokumentin sivumäärän hakeminen."""
        # Lataa PDF ja hae sivumäärä
        pdf_doc = pdf_repository.load_pdf(sample_pdf)
        
        try:
            page_count = pdf_repository.get_page_count(pdf_doc)
            assert page_count == 5
        finally:
            # Sulje dokumentti aina
            pdf_doc.close()

    def test_extract_pages(self, pdf_repository, sample_pdf):
        """Testaa sivujen poiminta PDF-dokumentista."""
        # Lataa PDF ja poimi sivut
        pdf_doc = pdf_repository.load_pdf(sample_pdf)
        
        try:
            # Poimitse ensimmäiset kaksi sivua
            extracted_doc = pdf_repository.extract_pages(pdf_doc, 0, 1)
            
            assert isinstance(extracted_doc, fitz.Document)
            assert extracted_doc.page_count == 2
            
            # Sulje poimittu dokumentti
            extracted_doc.close()
        finally:
            # Sulje alkuperäinen dokumentti aina
            pdf_doc.close()

    def test_save_pdf(self, pdf_repository, sample_pdf):
        """Testaa PDF-dokumentin tallentaminen."""
        # Lataa PDF ja tallenna uuteen sijaintiin
        pdf_doc = pdf_repository.load_pdf(sample_pdf)
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_output:
                # Tallenna PDF uuteen sijaintiin
                output_path = pdf_repository.save_pdf(pdf_doc, temp_output.name)
                
                # Varmista tallennus
                assert output_path == temp_output.name
                
                # Varmista tiedoston olemassaolo
                assert os.path.exists(output_path)
                
                # Varmista, että tallennettu PDF voidaan avata
                saved_doc = fitz.open(output_path)
                assert saved_doc.page_count == 5
                saved_doc.close()
        finally:
            # Sulje alkuperäinen dokumentti aina
            pdf_doc.close()
            
            # Poista väliaikainen tiedosto
            if 'temp_output' in locals() and not temp_output.closed:
                os.unlink(temp_output.name)

    def test_close_pdf(self, pdf_repository, sample_pdf):
        """Testaa PDF-dokumentin sulkeminen."""
        # Lataa PDF ja sulje se
        pdf_doc = pdf_repository.load_pdf(sample_pdf)
        
        # Sulje dokumentti
        pdf_repository.close_pdf(pdf_doc)
        
        # Varmista, että dokumentti on suljettu (aiheuttaa poikkeuksen, jos ei)
        with pytest.raises(ValueError):
            _ = pdf_doc.page_count