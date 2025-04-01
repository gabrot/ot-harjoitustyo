"""Apufunktioiden yksikkötestit."""
import pytest
from src.utils.helpers import (
    get_file_size_str, 
    create_pdf_preview, 
    validate_parts_count, 
    parse_page_ranges
)
import fitz
import tempfile
import os

class TestHelpers:
    """Testaa apufunktioiden toiminnallisuudet."""

    def test_get_file_size_str(self):
        """Testaa tiedoston koon muuntaminen luettavaan muotoon."""
        assert get_file_size_str(500) == "500.00 B"  # Päivitetty odotettu arvo
        assert get_file_size_str(1500) == "1.46 KB"
        assert get_file_size_str(1500000) == "1.43 MB"
        assert get_file_size_str(1500000000) == "1.40 GB"

    def test_validate_parts_count(self):
        """Testaa osien määrän validointi."""
        # Kelvolliset tapaukset
        assert validate_parts_count("") is True
        assert validate_parts_count("1") is True
        assert validate_parts_count("50") is True
        assert validate_parts_count("100") is True

        # Virheelliset tapaukset
        assert validate_parts_count("0") is False
        assert validate_parts_count("101") is False
        assert validate_parts_count("-5") is False
        assert validate_parts_count("abc") is False

    def test_parse_page_ranges_valid(self):
        """Testaa sivualueiden jäsentäminen kelvollisilla syötteillä."""
        # Luo testiä varten PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            doc = fitz.open()
            for _ in range(10):
                doc.new_page()
            doc.save(temp_file.name)
            doc.close()

        # Testaa eri sivualueiden jäsentämistä
        assert parse_page_ranges("1-3", 10) == [(1, 3)]
        assert parse_page_ranges("1, 3-5, 8", 10) == [(1, 1), (3, 5), (8, 8)]
        assert parse_page_ranges("1-10", 10) == [(1, 10)]

        # Poista väliaikainen tiedosto
        os.unlink(temp_file.name)

    def test_parse_page_ranges_invalid(self):
        """Testaa virheellisten sivualueiden käsittely."""
        # Virheelliset sivualueet
        assert parse_page_ranges("0-3", 10) is None
        assert parse_page_ranges("1-15", 10) is None
        assert parse_page_ranges("abc", 10) is None

    def test_create_pdf_preview(self):
        """Testaa PDF-esikatselukuvan luominen."""
        # Luo testiä varten PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            doc = fitz.open()
            doc.new_page()
            doc.save(temp_file.name)
            doc.close()

        try:
            # Alusta Tkinter root-ikkuna testejä varten
            import tkinter as tk
            root = tk.Tk()
            
            # Avaa PDF
            pdf_doc = fitz.open(temp_file.name)

            # Testaa esikatselukuvan luominen
            preview = create_pdf_preview(pdf_doc)
            assert preview is not None  # Olettaen, että palauttaa PhotoImage-olion tai vastaavan

            # Testaa mukautetulla leveydellä
            preview_custom = create_pdf_preview(pdf_doc, width=500)
            assert preview_custom is not None

            # Testaa virheellinen sivuindeksi
            preview_invalid = create_pdf_preview(pdf_doc, page_index=10)
            assert preview_invalid is None

            # Sulje Tkinter ikkuna
            root.destroy()
        finally:
            # Poista väliaikainen tiedosto
            os.unlink(temp_file.name)