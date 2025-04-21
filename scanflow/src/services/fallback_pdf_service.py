"""
Fallback-toteutus PDFSplitterService-luokalle.

Tätä moduulia käytetään vain tilanteissa, joissa varsinaista PDF-käsittelyä
ei voida suorittaa esim. puuttuvien kirjastojen vuoksi.
"""

import os
import time
from typing import List, Tuple, Callable, Optional


class FallbackPDFService:
    """
    Yksinkertainen fallback-toteutus PDFSplitterService-luokalle.

    Tämä luokka tarjoaa samat julkiset metodit kuin varsinainen PDFSplitterService,
    mutta ei tee oikeaa PDF-käsittelyä vaan simuloi operaatioita.
    """

    def get_pdf_info(self, file_path: str) -> dict:
        """
        Palauttaa simuloidun tietorakenteen PDF-tiedoston tiedoista.

        Args:
            file_path: PDF-tiedoston polku.

        Returns:
            Sanakirja simuloiduilla PDF-tiedoston tiedoilla.
        """
        time.sleep(0.5)

        return {
            "page_count": 10,
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
        }

    def split_by_fixed_range(
        self,
        file_path: str,
        _pages_per_file: int,
        output_dir: str,
        *,
        base_filename: Optional[str] = None,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> List[str]:
        """
        Simuloi PDF-tiedoston jakamista kiinteän sivumäärän mukaan.

        Args:
            file_path: PDF-tiedoston polku.
            pages_per_file: Sivujen määrä per tulostiedosto.
            output_dir: Hakemisto, johon tulostiedostot tallennetaan.
            base_filename: Tiedostonimen perusosa.
            progress_callback: Edistymistä seuraava callback-funktio.

        Returns:
            Lista simuloituja tulostiedostoja.
        """
        if base_filename is None:
            base_filename = os.path.splitext(os.path.basename(file_path))[0]

        total_parts = 3
        parts_done = 0

        for i in range(total_parts):
            time.sleep(0.7)
            parts_done += 1

            if progress_callback:
                progress_callback(int(parts_done / total_parts * 100))

        return [
            os.path.join(output_dir, f"{base_filename}_part{i + 1}.pdf")
            for i in range(total_parts)
        ]

    def split_by_custom_ranges(
        self,
        file_path: str,
        ranges: List[Tuple[int, int]],
        output_dir: str,
        *,
        base_filename: Optional[str] = None,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> List[str]:
        """
        Simuloi PDF-tiedoston jakamista mukautettujen sivualueiden mukaan.

        Args:
            file_path: PDF-tiedoston polku.
            ranges: Lista mukautettuja sivualueita (alku, loppu) -pareina.
            output_dir: Hakemisto, johon tulostiedostot tallennetaan.
            base_filename: Tiedostonimen perusosa.
            progress_callback: Edistymistä seuraava callback-funktio.

        Returns:
            Lista simuloituja tulostiedostoja.
        """
        if base_filename is None:
            base_filename = os.path.splitext(os.path.basename(file_path))[0]

        total_parts = len(ranges)
        parts_done = 0

        for i in range(total_parts):
            time.sleep(0.6)
            parts_done += 1

            if progress_callback:
                progress_callback(int(parts_done / total_parts * 100))

        return [
            os.path.join(output_dir, f"{base_filename}_custom_part{i + 1}.pdf")
            for i in range(total_parts)
        ]
