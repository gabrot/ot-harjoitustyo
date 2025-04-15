"""Moduuli PDF-dokumenttien käsittelyyn matalan tason operaatioilla.

Tarjoaa `PDFRepository`-luokan, joka kapseloi PDF-tiedostojen
lataamisen, sivujen poimimisen, tallentamisen ja sulkemisen
käyttäen PyMuPDF (fitz) -kirjastoa.
"""

import os
import fitz # PyMuPDF
from typing import Dict, Any


class PDFRepository:
    """Repositorio PDF-dokumenttien käsittelyyn PyMuPDF-kirjaston avulla.

    Tarjoaa keskitetyn rajapinnan PDF-tiedostojen perusoperaatioille.
    Hoitaa virheenkäsittelyn liittyen tiedosto-operaatioihin.
    """

    def load_pdf(self, file_path: str) -> fitz.Document:
        """Lataa PDF-dokumentin annetusta tiedostopolusta.

        Args:
            file_path: Ladattavan PDF-tiedoston polku.

        Returns:
            PyMuPDF-dokumenttiobjekti ladatusta tiedostosta.

        Raises:
            FileNotFoundError: Jos annettua tiedostoa ei löydy.
            ValueError: Jos tiedoston avaaminen epäonnistuu (esim. ei ole
                        kelvollinen PDF tai lukuoikeuksia ei ole).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Tiedostoa ei löydy: {file_path}")

        pdf_document = None
        try:
            pdf_document = fitz.open(file_path)
            if not pdf_document.is_pdf:
                if pdf_document:
                    pdf_document.close()
                raise ValueError(f"Tiedosto ei ole kelvollinen PDF: {file_path}")
            return pdf_document
        except Exception as e:
            if pdf_document and not pdf_document.is_closed:
                pdf_document.close()
            raise ValueError(
                f"PDF-tiedoston ({os.path.basename(file_path)}) avaaminen epäonnistui: {e}"
            ) from e

    def get_page_count(self, pdf_document: fitz.Document) -> int:
        """Palauttaa annetun PDF-dokumentin sivujen kokonaismäärän.

        Args:
            pdf_document: PyMuPDF-dokumenttiobjekti.

        Returns:
            Dokumentin sivumäärä.

        Raises:
            ValueError: Jos annettu dokumenttiobjekti on suljettu tai virheellinen.
        """
        if pdf_document.is_closed:
            raise ValueError("Dokumentti on suljettu.")
        return pdf_document.page_count

    def get_metadata(self, pdf_document: fitz.Document) -> Dict[str, Any]:
        """Palauttaa PDF-dokumentin metatiedot sanakirjana.

        Args:
            pdf_document: PyMuPDF-dokumenttiobjekti.

        Returns:
            Sanakirja, joka sisältää dokumentin metatiedot (voi olla tyhjä).
            Mahdollisia avaimia: 'format', 'title', 'author', 'subject',
            'keywords', 'creator', 'producer', 'creationDate', 'modDate'.

        Raises:
            ValueError: Jos annettu dokumenttiobjekti on suljettu.
        """
        if pdf_document.is_closed:
            raise ValueError("Dokumentti on suljettu.")
        return pdf_document.metadata or {}

    def extract_pages(
        self, pdf_document: fitz.Document, start_page: int, end_page: int
    ) -> fitz.Document:
        """Poimii määritellyt sivut annetusta PDF-dokumentista uuteen dokumenttiin.

        Args:
            pdf_document: Alkuperäinen PyMuPDF-dokumentti.
            start_page: Ensimmäisen poimittavan sivun indeksi (0-pohjainen).
            end_page: Viimeisen poimittavan sivun indeksi (0-pohjainen, sisällytetty).

        Returns:
            Uusi PyMuPDF-dokumentti, joka sisältää vain poimitut sivut.
            Palauttaa tyhjän dokumentin, jos indeksit ovat virheelliset siten,
            että yhtään sivua ei voida poimia.

        Raises:
             ValueError: Jos alkuperäinen dokumentti on suljettu.
        """
        if pdf_document.is_closed:
            raise ValueError("Alkuperäinen dokumentti on suljettu.")

        page_count = self.get_page_count(pdf_document)
        start_page = max(0, start_page)
        end_page = min(page_count - 1, end_page)

        if start_page > end_page:
            return fitz.open()

        new_doc = fitz.open()
        try:
            new_doc.insert_pdf(pdf_document, from_page=start_page, to_page=end_page)
            return new_doc
        except Exception as e:
            new_doc.close()
            raise ValueError(
                f"Sivujen {start_page + 1}-{end_page + 1} poiminta epäonnistui: {e}"
            ) from e

    def save_pdf(self, pdf_document: fitz.Document, output_path: str) -> str:
        """Tallentaa annetun PDF-dokumentin määritettyyn tiedostopolkuun.

        Args:
            pdf_document: Tallennettava PyMuPDF-dokumentti.
            output_path: Tiedostopolku, johon dokumentti tallennetaan.

        Returns:
            Tallennetun tiedoston täydellinen polku.

        Raises:
            ValueError: Jos dokumentti on suljettu.
            IOError: Jos hakemistoa ei voida luoda tai kirjoitusoikeuksia ei ole.
            Exception: Muut fitz.Document.save()-metodin nostamat virheet.
        """
        if pdf_document.is_closed:
            raise ValueError("Tallennettava dokumentti on suljettu.")

        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except OSError as e:
                    raise IOError(
                        f"Kohdehakemiston '{output_dir}' luominen epäonnistui: {e}"
                    ) from e

            pdf_document.save(output_path, garbage=4, deflate=True)
            return output_path
        except Exception as e:
            raise Exception(
                f"PDF-dokumentin tallennus polkuun '{output_path}' epäonnistui: {e}"
            ) from e

    def close_pdf(self, pdf_document: fitz.Document | None):
        """Sulkee annetun PDF-dokumentin ja vapauttaa sen resurssit.

        Args:
            pdf_document: Suljettava PyMuPDF-dokumentti tai None.
        """

        if pdf_document and not pdf_document.is_closed:
            try:
                pdf_document.close()
            except Exception:
                pass
