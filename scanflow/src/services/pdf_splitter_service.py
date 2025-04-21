"""
Palveluluokka PDF-tiedostojen jakamiseen.

Tarjoaa korkeamman tason toiminnallisuuden PDF-tiedostojen jakamiseen
käyttäen `PDFRepository`-luokkaa tiedosto-operaatioihin. Pystyy jakamaan
PDF:n joko kiinteän sivumäärän mukaan tai käyttäjän määrittelemien
mukautettujen sivualueiden perusteella.
"""

import math
import os
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, TypedDict

from ..repositories.pdf_repository import PDFRepository


class OutputConfig(TypedDict):
    """
    Tulostusasetusten tyyppi PDF-jakamisoperaatioille.

    Attributes:
        dir: Hakemistopolku, johon tiedostot tallennetaan
        base_filename: Tiedostonimen perusosa (ilman päätettä)
        formatter: Funktio, joka muodostaa tiedoston nimen
        original_file_path: Alkuperäisen tiedoston polku
    """

    dir: str
    base_filename: str
    formatter: Callable
    original_file_path: str


class PDFSplitterService:
    """Palvelu PDF-tiedostojen jakamiseen eri kriteereillä."""

    def __init__(self, pdf_repository: Optional[PDFRepository] = None):
        """
        Alustaa PDF-jakamispalvelun.

        Args:
            pdf_repository: Valinnainen PDFRepository-instanssi. Jos None,
                           luodaan uusi instanssi.
        """
        self.pdf_repository = pdf_repository or PDFRepository()

    def get_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """
        Hakee ja palauttaa perustiedot annetusta PDF-tiedostosta.

        Args:
            file_path: PDF-tiedoston polku.

        Returns:
            Sanakirja, joka sisältää tiedoston perustiedot: sivumäärä,
            tiedostopolku ja tiedoston nimi.
        """
        with self._open_source_pdf(file_path) as pdf_document:
            page_count = self.pdf_repository.get_page_count(pdf_document)
            return {
                "page_count": page_count,
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
            }

    @contextmanager
    def _open_source_pdf(self, file_path: str) -> Iterator[Any]:
        """
        Avaa lähde-PDF:n ja varmistaa sen sulkemisen context managerilla.

        Args:
            file_path: Avattavan PDF-tiedoston polku.

        Yields:
            Avattu PDF-dokumentti.
        """
        pdf_document = None
        try:
            pdf_document = self.pdf_repository.load_pdf(file_path)
            yield pdf_document
        finally:
            if pdf_document:
                self.pdf_repository.close_pdf(pdf_document)

    def _extract_and_save_part(
        self,
        source_doc: Any,
        start_idx: int,
        end_idx: int,
        output_path: str,
    ) -> None:
        """
        Poimii sivut, tallentaa osatiedoston ja sulkee sen.

        Args:
            source_doc: Lähde-PDF-dokumentti.
            start_idx: Aloitussivun indeksi (0-pohjainen).
            end_idx: Lopetussivun indeksi (0-pohjainen).
            output_path: Kohdetiedoston polku.
        """
        new_doc = None
        try:
            new_doc = self.pdf_repository.extract_pages(source_doc, start_idx, end_idx)
            self.pdf_repository.save_pdf(new_doc, output_path)
        finally:
            if new_doc:
                self.pdf_repository.close_pdf(new_doc)

    def _format_fixed_output_filename(
        self, base_filename: str, part_info: Tuple[int, int, int, int]
    ) -> str:
        """
        Muotoilee tiedostonimen kiinteän jaon osalle.

        Args:
            base_filename: Pohjatiedoston nimi ilman tiedostopäätettä.
            part_info: Tuple, joka sisältää (start_idx, end_idx, start_page_user, end_page_user).

        Returns:
            Muotoiltu tiedostonimi kiinteän jaon osalle.
        """
        _start_idx, _end_idx, start_page_user, end_page_user = part_info
        return f"{base_filename}_sivut_{start_page_user}-{end_page_user}.pdf"

    def _format_custom_output_filename(
        self, base_filename: str, part_info: Tuple[int, int, int, int, int]
    ) -> str:
        """
        Muotoilee tiedostonimen mukautetun jaon osalle.

        Args:
            base_filename: Pohjatiedoston nimi ilman tiedostopäätettä.
            part_info: Tuple, joka sisältää 
            (index, start_idx, end_idx, start_page_user, end_page_user).

        Returns:
            Muotoiltu tiedostonimi mukautetun jaon osalle.
        """
        index, _start_idx, _end_idx, start_page_user, end_page_user = part_info
        return f"{base_filename}_alue_{index + 1}_sivut_{start_page_user}-{end_page_user}.pdf"

    def _validate_custom_range(
        self, start_user: int, end_user: int, page_count: int
    ) -> None:
        """
        Tarkistaa mukautetun alueen kelvollisuuden.

        Args:
            start_user: Käyttäjän antama aloitussivun numero (1-pohjainen).
            end_user: Käyttäjän antama lopetussivun numero (1-pohjainen).
            page_count: Dokumentin kokonaissivumäärä.

        Raises:
            ValueError: Jos annettu alue on virheellinen tai rajojen ulkopuolella.
        """
        start_idx = start_user - 1
        end_idx = end_user - 1
        if not (
            0 <= start_idx < page_count
            and 0 <= end_idx < page_count
            and start_idx <= end_idx
        ):
            error_msg_part1 = (
                f"Virheellinen tai rajojen ulkopuolinen alue: "
                f"{start_user}-{end_user}."
            )
            error_msg_part2 = f"Sivuja dokumentissa: 1-{page_count}"
            raise ValueError(error_msg_part1 + error_msg_part2)

    def _fixed_range_part_iterator(
        self, page_count: int, pages_per_file: int
    ) -> Iterator[Tuple[int, int, int, int]]:
        """
        Generaattori kiinteän jaon osien indeksien ja sivunumeroiden luomiseen.

        Args:
            page_count: Dokumentin kokonaissivumäärä.
            pages_per_file: Sivujen määrä tiedostoa kohden.

        Yields:
            Tuple (start_idx, end_idx, start_page_user, end_page_user), jossa
            start_idx ja end_idx ovat 0-pohjaisia indeksejä ja
            start_page_user ja end_page_user ovat käyttäjälle näytettäviä
            1-pohjaisia numeroita.
        """
        if page_count == 0:
            return
        for i in range(math.ceil(page_count / pages_per_file)):
            start_idx = i * pages_per_file
            end_idx = min((i + 1) * pages_per_file - 1, page_count - 1)
            yield start_idx, end_idx, start_idx + 1, end_idx + 1

    def _custom_range_part_iterator(
        self, page_count: int, ranges: List[Tuple[int, int]]
    ) -> Iterator[Tuple[int, int, int, int, int]]:
        """
        Generaattori mukautettujen osien indeksien ja sivunumeroiden luomiseen.

        Args:
            page_count: Dokumentin kokonaissivumäärä.
            ranges: Lista (aloitussivu, lopetussivu) -tupleja, jossa sivunumerot ovat 1-pohjaisia.

        Yields:
            Tuple (i, start_idx, end_idx, start_user, end_user), jossa
            i on järjestysnumero, start_idx ja end_idx ovat 0-pohjaisia indeksejä ja
            start_user ja end_user ovat käyttäjän antamia 1-pohjaisia sivunumeroita.

        Raises:
            ValueError: Jos dokumentti on tyhjä mutta alueita yritetään määrittää.
        """
        if page_count == 0 and ranges:
            raise ValueError("Cannot split an empty document based on ranges.")
        for i, (start_user, end_user) in enumerate(ranges):
            self._validate_custom_range(start_user, end_user, page_count)
            start_idx = start_user - 1
            end_idx = end_user - 1
            yield i, start_idx, end_idx, start_user, end_user

    def _process_single_part(
        self,
        source_doc: Any,
        output_config: OutputConfig,
        part_info: Tuple,
    ) -> str:
        """
        Käsittelee yhden osan jaon: poimii sivut ja tallentaa tiedoston.

        Args:
            source_doc: Lähde-PDF-dokumentti.
            output_config: Asetukset tulostusta varten.
            part_info: Tiedot käsiteltävästä osasta (iteratorin tuottama).

        Returns:
            Luodun tiedoston polku.
        """
        is_custom_range = len(part_info) == 5
        start_idx = part_info[1] if is_custom_range else part_info[0]
        end_idx = part_info[2] if is_custom_range else part_info[1]

        output_dir = output_config["dir"]
        filename_formatter = output_config["formatter"]
        original_file_path = output_config["original_file_path"]
        true_base_filename = os.path.splitext(os.path.basename(original_file_path))[0]

        output_filename = filename_formatter(true_base_filename, part_info)
        output_path = os.path.join(output_dir, output_filename)

        self._extract_and_save_part(source_doc, start_idx, end_idx, output_path)
        return output_path

    def _process_split_parts(
        self,
        source_doc: Any,
        output_config: OutputConfig,
        part_iterator: Iterator[Tuple],
        *,
        progress_callback: Optional[Callable[[int], None]],
        total_parts: int,
    ) -> List[str]:
        """
        Käsittelee osien jaon pääsilmukan.

        Args:
            source_doc: Lähde-PDF-dokumentti.
            output_config: Asetukset tulostusta varten.
            part_iterator: Iteraattori, joka tuottaa osat.
            progress_callback: Valinnainen edistymisen raportointi -callback.
            total_parts: Osien kokonaismäärä.

        Returns:
            Lista luotujen tiedostojen polkuja.
        """
        output_files = []
        if total_parts == 0:
            return []

        for parts_done, part_info in enumerate(part_iterator, 1):
            output_path = self._process_single_part(
                source_doc, output_config, part_info
            )
            output_files.append(output_path)

            if progress_callback:
                progress = int((parts_done / total_parts) * 100)
                progress_callback(progress)

        return output_files

    def split_by_fixed_range(
        self,
        file_path: str,
        pages_per_file: int,
        output_dir: str,
        *,
        base_filename: Optional[str] = None,
        progress_callback: Optional[Callable[[int], None]] = None,
    ) -> List[str]:
        """
        Jakaa PDF-tiedoston osiin, joissa on kiinteä määrä sivuja.

        Args:
            file_path: PDF-tiedoston polku.
            pages_per_file: Sivujen määrä tiedostoa kohden.
            output_dir: Kohdepolku, johon tiedostot tallennetaan.
            base_filename: Valinnainen tulostiedostojen perusnimi.
            progress_callback: Valinnainen edistymisen raportointi -callback.

        Returns:
            Lista luotujen tiedostojen polkuja.

        Raises:
            ValueError: Jos pages_per_file on alle 1.
            IOError: Jos tulostushakemistoa ei löydy.
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

        with self._open_source_pdf(file_path) as pdf_document:
            page_count = self.pdf_repository.get_page_count(pdf_document)
            part_iterator = self._fixed_range_part_iterator(page_count, pages_per_file)
            total_parts = (
                math.ceil(page_count / pages_per_file) if page_count > 0 else 0
            )

            output_config: OutputConfig = {
                "dir": output_dir,
                "base_filename": final_base_filename,
                "formatter": self._format_fixed_output_filename,
                "original_file_path": file_path,
            }

            output_files = self._process_split_parts(
                source_doc=pdf_document,
                output_config=output_config,
                part_iterator=part_iterator,
                progress_callback=progress_callback,
                total_parts=total_parts,
            )
        return output_files

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
        Jakaa PDF-tiedoston osiin käyttäjän määrittelemien sivualueiden mukaan.

        Args:
            file_path: PDF-tiedoston polku.
            ranges: Lista (aloitussivu, lopetussivu) -tupleja, jossa sivunumerot ovat 1-pohjaisia.
            output_dir: Kohdepolku, johon tiedostot tallennetaan.
            base_filename: Valinnainen tulostiedostojen perusnimi.
            progress_callback: Valinnainen edistymisen raportointi -callback.

        Returns:
            Lista luotujen tiedostojen polkuja.

        Raises:
            ValueError: Jos ei ole määritetty yhtään sivualuetta.
            IOError: Jos tulostushakemistoa ei löydy.
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

        with self._open_source_pdf(file_path) as pdf_document:
            page_count = self.pdf_repository.get_page_count(pdf_document)
            part_iterator = self._custom_range_part_iterator(page_count, ranges)
            total_parts = len(ranges)

            output_config: OutputConfig = {
                "dir": output_dir,
                "base_filename": final_base_filename,
                "formatter": self._format_custom_output_filename,
                "original_file_path": file_path,
            }

            output_files = self._process_split_parts(
                source_doc=pdf_document,
                output_config=output_config,
                part_iterator=part_iterator,
                progress_callback=progress_callback,
                total_parts=total_parts,
            )
        return output_files
