"""Palveluluokka PDF-tiedostojen jakamiseen.

Tarjoaa korkeamman tason toiminnallisuuden PDF-tiedostojen jakamiseen
käyttäen `PDFRepository`-luokkaa tiedosto-operaatioihin. Pystyy jakamaan
PDF:n joko kiinteän sivumäärän mukaan tai käyttäjän määrittelemien
mukautettujen sivualueiden perusteella.
"""

import os
import math
from typing import List, Tuple, Dict, Optional, Any, Callable
from repositories.pdf_repository import PDFRepository


class PDFSplitterService:
    """Palvelu PDF-tiedostojen jakamiseen eri kriteereillä.

    Attributes:
        pdf_repository (PDFRepository): Instanssi PDF-tiedostojen käsittelyyn.
    """

    def __init__(self, pdf_repository: Optional[PDFRepository] = None):
        """Alustaa PDF-jakamispalvelun.

        Args:
            pdf_repository: Valmis PDFRepository-instanssi. Jos None, luodaan uusi.
        """
        self.pdf_repository = pdf_repository or PDFRepository()

    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """Hakee ja palauttaa perustiedot annetusta PDF-tiedostosta.

        Args:
            file_path: Polku PDF-tiedostoon.

        Returns:
            Sanakirja, joka sisältää avaimet 'page_count', 'file_path', 'file_name'.

        Raises:
            FileNotFoundError: Jos tiedostoa ei löydy.
            ValueError: Jos tiedosto ei ole kelvollinen PDF tai avaaminen epäonnistuu.
        """
        pdf_document = None
        try:
            pdf_document = self.pdf_repository.load_pdf(file_path)
            page_count = self.pdf_repository.get_page_count(pdf_document)
            return {
                "page_count": page_count,
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
            }
        finally:
            if pdf_document:
                self.pdf_repository.close_pdf(pdf_document)

    def split_by_fixed_range(
        self,
        file_path: str,
        pages_per_file: int,
        output_dir: str,
        base_filename: Optional[str] = None,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> List[str]:
        """Jakaa PDF-tiedoston osiin, joissa on kiinteä määrä sivuja.

        Args:
            file_path: Alkuperäisen PDF-tiedoston polku.
            pages_per_file: Sivujen määrä kuhunkin uuteen tiedostoon (>= 1).
            output_dir: Hakemisto, johon jaetut tiedostot tallennetaan.
            base_filename: Tulostiedostojen nimen perusosa. Jos None, käytetään alkuperäistä.
            progress_callback: Funktio, jota kutsutaan edistymisen päivittämiseksi (0-100).

        Returns:
            Lista luotujen uusien PDF-tiedostojen poluista.

        Raises:
            FileNotFoundError, ValueError, IOError: Virhetilanteissa.
        """
        if pages_per_file < 1:
            raise ValueError("Sivujen määrän per tiedosto tulee olla vähintään 1.")
        if not os.path.isdir(output_dir):
            raise IOError(
                f"Tulostushakemistoa ei löydy tai se ei ole hakemisto: {output_dir}"
            )

        final_base_filename = (
            base_filename or os.path.splitext(os.path.basename(file_path))[0]
        )

        pdf_document = None
        output_files = []
        try:
            pdf_document = self.pdf_repository.load_pdf(file_path)
            page_count = self.pdf_repository.get_page_count(pdf_document)
            total_parts = math.ceil(page_count / pages_per_file)
            parts_done = 0

            for i in range(0, page_count, pages_per_file):
                start_page_idx = i
                end_page_idx = min(i + pages_per_file - 1, page_count - 1)

                if start_page_idx > end_page_idx:
                    continue

                new_doc = None
                try:
                    new_doc = self.pdf_repository.extract_pages(
                        pdf_document, start_page_idx, end_page_idx
                    )
                    output_filename = (
                        f"{final_base_filename}_sivut_{start_page_idx + 1}-"
                        f"{end_page_idx + 1}.pdf"
                    )
                    output_path = os.path.join(output_dir, output_filename)
                    self.pdf_repository.save_pdf(new_doc, output_path)
                    output_files.append(output_path)
                    parts_done += 1
                    if progress_callback:
                        progress = int((parts_done / total_parts) * 100)
                        progress_callback(progress)
                finally:
                    if new_doc:
                        self.pdf_repository.close_pdf(new_doc)
        finally:
            if pdf_document:
                self.pdf_repository.close_pdf(pdf_document)
        return output_files

    def split_by_custom_ranges(
        self,
        file_path: str,
        ranges: List[Tuple[int, int]],
        output_dir: str,
        base_filename: Optional[str] = None,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> List[str]:
        """Jakaa PDF-tiedoston osiin käyttäjän määrittelemien sivualueiden mukaan.

        Args:
            file_path: Alkuperäisen PDF-tiedoston polku.
            ranges: Lista tupleja (alkusivu, loppusivu). Sivunumerot 1-pohjaisia.
            output_dir: Hakemisto, johon jaetut tiedostot tallennetaan.
            base_filename: Tulostiedostojen nimen perusosa. Jos None, käytetään alkuperäistä.
            progress_callback: Funktio, jota kutsutaan edistymisen päivittämiseksi (0-100).

        Returns:
            Lista luotujen uusien PDF-tiedostojen poluista.

        Raises:
            FileNotFoundError, ValueError, IOError: Virhetilanteissa.
            ValueError: Jos yksikin annettu alue on virheellinen.
        """
        if not ranges:
            raise ValueError("Vähintään yksi sivualue on määritettävä.")
        if not os.path.isdir(output_dir):
            raise IOError(
                f"Tulostushakemistoa ei löydy tai se ei ole hakemisto: {output_dir}"
            )

        final_base_filename = (
            base_filename or os.path.splitext(os.path.basename(file_path))[0]
        )

        pdf_document = None
        output_files = []
        try:
            pdf_document = self.pdf_repository.load_pdf(file_path)
            page_count = self.pdf_repository.get_page_count(pdf_document)
            total_parts = len(ranges)
            parts_done = 0

            for i, (start_user, end_user) in enumerate(ranges):
                start_idx = start_user - 1
                end_idx = end_user - 1

                if not (
                    0 <= start_idx < page_count
                    and 0 <= end_idx < page_count
                    and start_idx <= end_idx
                ):
                    raise ValueError(
                        f"Virheellinen tai rajojen ulkopuolinen alue: {start_user}-{end_user}. "
                        f"Sivuja dokumentissa: 1-{page_count}"
                    )

                new_doc = None
                try:
                    new_doc = self.pdf_repository.extract_pages(
                        pdf_document, start_idx, end_idx
                    )
                    output_filename = (
                        f"{final_base_filename}_alue_{i + 1}_sivut_{start_user}-{end_user}.pdf"
                    )
                    output_path = os.path.join(output_dir, output_filename)
                    self.pdf_repository.save_pdf(new_doc, output_path)
                    output_files.append(output_path)
                    parts_done += 1
                    if progress_callback:
                        progress = int((parts_done / total_parts) * 100)
                        progress_callback(progress)
                finally:
                    if new_doc:
                        self.pdf_repository.close_pdf(new_doc)
        finally:
            if pdf_document:
                self.pdf_repository.close_pdf(pdf_document)
        return output_files
