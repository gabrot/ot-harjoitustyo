import unittest
from unittest.mock import patch, MagicMock, call
import os
import math

import sys

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from services.pdf_splitter_service import PDFSplitterService
from repositories.pdf_repository import PDFRepository


class TestPDFSplitterService(unittest.TestCase):
    """Testiluokka PDFSplitterService-luokan toiminnallisuuksien testaamiseen."""

    def setUp(self):
        """Alustaa testitapaukset luomalla mock PDFRepositoryn ja palvelun."""
        self.mock_repository = MagicMock(spec=PDFRepository)
        self.service = PDFSplitterService(pdf_repository=self.mock_repository)

        self.test_file_path = os.path.join("dummy", "input", "test_document.pdf")
        self.output_dir = os.path.join("dummy", "output")
        self.base_filename = "split_doc"

        self.mock_loaded_doc = MagicMock()
        self.mock_extracted_doc = MagicMock()
        self.mock_loaded_doc.close = MagicMock()
        self.mock_extracted_doc.close = MagicMock()

        self.mock_repository.load_pdf.return_value = self.mock_loaded_doc
        self.mock_repository.get_page_count.return_value = 10
        self.mock_repository.extract_pages.return_value = self.mock_extracted_doc
        self.mock_repository.close_pdf = MagicMock()

    def test_init_without_repository(self):
        """Testaa, että palvelu luo oman PDFRepositoryn, jos sitä ei anneta."""
        with patch("services.pdf_splitter_service.PDFRepository") as MockRepo:
            instance = MockRepo.return_value
            service = PDFSplitterService()
            self.assertIsNotNone(service.pdf_repository)
            self.assertIs(service.pdf_repository, instance)
            MockRepo.assert_called_once()

    def test_init_with_repository(self):
        """Testaa, että palvelu käyttää annettua repository-instanssia."""
        with patch("services.pdf_splitter_service.PDFRepository") as MockRepoCheck:
            mock_repo_provided = MagicMock(spec=PDFRepository)
            service = PDFSplitterService(pdf_repository=mock_repo_provided)
            self.assertIs(service.pdf_repository, mock_repo_provided)
            MockRepoCheck.assert_not_called()

    def test_get_pdf_info_success(self):
        """Testaa PDF-tiedoston perustietojen onnistunutta hakua."""
        self.mock_repository.get_page_count.return_value = 15
        result = self.service.get_pdf_info(self.test_file_path)
        expected_result = {
            "page_count": 15,
            "file_path": self.test_file_path,
            "file_name": os.path.basename(self.test_file_path),
        }
        self.assertEqual(result, expected_result)
        self.mock_repository.load_pdf.assert_called_once_with(self.test_file_path)
        self.mock_repository.get_page_count.assert_called_once_with(
            self.mock_loaded_doc
        )
        self.mock_repository.close_pdf.assert_called_once_with(self.mock_loaded_doc)

    def test_get_pdf_info_load_failure(self):
        """Testaa virheen käsittelyä, kun PDF:n lataus epäonnistuu."""
        self.mock_repository.load_pdf.side_effect = FileNotFoundError(
            "Tiedostoa ei löytynyt"
        )
        with self.assertRaises(FileNotFoundError):
            self.service.get_pdf_info(self.test_file_path)
        self.mock_repository.load_pdf.assert_called_once_with(self.test_file_path)
        self.mock_repository.close_pdf.assert_not_called()

    @patch("os.path.isdir", return_value=True)
    def test_split_by_fixed_range_success(self, mock_isdir):
        """Testaa PDF:n jakamista onnistuneesti kiinteällä sivumäärällä."""
        pages_per_file = 3
        self.mock_repository.get_page_count.return_value = 7
        expected_paths = [
            os.path.join(self.output_dir, f"{self.base_filename}_sivut_1-3.pdf"),
            os.path.join(self.output_dir, f"{self.base_filename}_sivut_4-6.pdf"),
            os.path.join(self.output_dir, f"{self.base_filename}_sivut_7-7.pdf"),
        ]

        mock_doc1 = MagicMock()
        mock_doc2 = MagicMock()
        mock_doc3 = MagicMock()
        mock_docs_returned = [mock_doc1, mock_doc2, mock_doc3]
        self.mock_repository.extract_pages.side_effect = mock_docs_returned

        result = self.service.split_by_fixed_range(
            self.test_file_path, pages_per_file, self.output_dir, self.base_filename
        )
        self.assertEqual(result, expected_paths)
        mock_isdir.assert_called_once_with(self.output_dir)
        self.mock_repository.load_pdf.assert_called_once_with(self.test_file_path)
        self.mock_repository.get_page_count.assert_called_once_with(
            self.mock_loaded_doc
        )

        expected_extract_calls = [
            call(self.mock_loaded_doc, 0, 2),
            call(self.mock_loaded_doc, 3, 5),
            call(self.mock_loaded_doc, 6, 6),
        ]
        self.assertEqual(
            self.mock_repository.extract_pages.call_args_list, expected_extract_calls
        )

        expected_save_calls = [
            call(mock_doc1, expected_paths[0]),
            call(mock_doc2, expected_paths[1]),
            call(mock_doc3, expected_paths[2]),
        ]
        self.assertEqual(
            self.mock_repository.save_pdf.call_args_list, expected_save_calls
        )

        expected_close_calls = [
            call(mock_doc1),
            call(mock_doc2),
            call(mock_doc3),
            call(self.mock_loaded_doc),
        ]
        self.mock_repository.close_pdf.assert_has_calls(
            expected_close_calls, any_order=True
        )
        self.assertEqual(
            self.mock_repository.close_pdf.call_count, len(mock_docs_returned) + 1
        )

    @patch("os.path.isdir", return_value=True)
    def test_split_by_fixed_range_exact_division(self, mock_isdir):
        """Testaa jakoa kiinteällä sivumäärällä, kun sivumäärä on jaollinen."""
        pages_per_file = 2
        self.mock_repository.get_page_count.return_value = 6
        result = self.service.split_by_fixed_range(
            self.test_file_path, pages_per_file, self.output_dir, self.base_filename
        )
        self.assertEqual(len(result), 3)
        self.assertEqual(
            self.mock_repository.extract_pages.call_args_list[-1],
            call(self.mock_loaded_doc, 4, 5),
        )

    @patch("os.path.isdir", return_value=True)
    def test_split_by_fixed_range_single_file(self, mock_isdir):
        """Testaa jakoa, kun sivuja per tiedosto on enemmän kuin dokumentissa sivuja."""
        pages_per_file = 15
        self.mock_repository.get_page_count.return_value = 10
        single_mock_doc = MagicMock()
        self.mock_repository.extract_pages.return_value = single_mock_doc

        result = self.service.split_by_fixed_range(
            self.test_file_path, pages_per_file, self.output_dir, self.base_filename
        )

        self.assertEqual(len(result), 1)
        self.mock_repository.extract_pages.assert_called_once_with(
            self.mock_loaded_doc, 0, 9
        )
        expected_path = os.path.join(
            self.output_dir, f"{self.base_filename}_sivut_1-10.pdf"
        )
        self.assertEqual(result[0], expected_path)
        expected_close_calls = [call(single_mock_doc), call(self.mock_loaded_doc)]
        self.mock_repository.close_pdf.assert_has_calls(
            expected_close_calls, any_order=True
        )
        self.assertEqual(self.mock_repository.close_pdf.call_count, 2)

    @patch("os.path.isdir", return_value=True)
    def test_split_by_fixed_range_with_progress_callback(self, mock_isdir):
        """Testaa, että edistymisen callback-funktiota kutsutaan oikein jaon aikana."""
        pages_per_file = 4
        self.mock_repository.get_page_count.return_value = 10
        mock_callback = MagicMock()
        self.service.split_by_fixed_range(
            self.test_file_path,
            pages_per_file,
            self.output_dir,
            self.base_filename,
            mock_callback,
        )
        total_parts = math.ceil(10 / pages_per_file)
        self.assertEqual(mock_callback.call_count, total_parts)
        mock_callback.assert_called_with(100)

    def test_split_by_fixed_range_invalid_pages_per_file(self):
        """Testaa virheen käsittelyä, kun sivuja per tiedosto on alle 1."""
        with self.assertRaisesRegex(
            ValueError, "Sivujen määrän per tiedosto tulee olla vähintään 1."
        ):
            self.service.split_by_fixed_range(self.test_file_path, 0, self.output_dir)

    @patch("os.path.isdir", return_value=False)
    def test_split_by_fixed_range_invalid_output_dir(self, mock_isdir):
        """Testaa virheen käsittelyä, kun tulostushakemisto on virheellinen."""
        with self.assertRaisesRegex(
            IOError, f"Tulostushakemistoa ei löydy.*: {self.output_dir}"
        ):
            self.service.split_by_fixed_range(self.test_file_path, 2, self.output_dir)
        mock_isdir.assert_called_once_with(self.output_dir)

    @patch("os.path.isdir", return_value=True)
    def test_split_by_custom_ranges_success(self, mock_isdir):
        """Testaa PDF:n jakamista onnistuneesti mukautetuilla sivualueilla."""
        ranges = [(1, 3), (5, 5), (8, 10)]
        self.mock_repository.get_page_count.return_value = 10
        expected_paths = [
            os.path.join(self.output_dir, f"{self.base_filename}_alue_1_sivut_1-3.pdf"),
            os.path.join(self.output_dir, f"{self.base_filename}_alue_2_sivut_5-5.pdf"),
            os.path.join(
                self.output_dir, f"{self.base_filename}_alue_3_sivut_8-10.pdf"
            ),
        ]
        mock_doc1 = MagicMock()
        mock_doc2 = MagicMock()
        mock_doc3 = MagicMock()
        mock_docs_returned = [mock_doc1, mock_doc2, mock_doc3]
        self.mock_repository.extract_pages.side_effect = mock_docs_returned

        result = self.service.split_by_custom_ranges(
            self.test_file_path, ranges, self.output_dir, self.base_filename
        )
        self.assertEqual(result, expected_paths)
        mock_isdir.assert_called_once_with(self.output_dir)
        self.mock_repository.load_pdf.assert_called_once_with(self.test_file_path)
        self.mock_repository.get_page_count.assert_called_once_with(
            self.mock_loaded_doc
        )

        expected_extract_calls = [
            call(self.mock_loaded_doc, 0, 2),
            call(self.mock_loaded_doc, 4, 4),
            call(self.mock_loaded_doc, 7, 9),
        ]
        self.assertEqual(
            self.mock_repository.extract_pages.call_args_list, expected_extract_calls
        )
        expected_save_calls = [
            call(mock_doc1, expected_paths[0]),
            call(mock_doc2, expected_paths[1]),
            call(mock_doc3, expected_paths[2]),
        ]
        self.assertEqual(
            self.mock_repository.save_pdf.call_args_list, expected_save_calls
        )

        expected_close_calls = [
            call(mock_doc1),
            call(mock_doc2),
            call(mock_doc3), 
            call(self.mock_loaded_doc),  
        ]
        self.mock_repository.close_pdf.assert_has_calls(
            expected_close_calls, any_order=True
        )
        self.assertEqual(
            self.mock_repository.close_pdf.call_count, len(mock_docs_returned) + 1
        )

    @patch("os.path.isdir", return_value=True)
    def test_split_by_custom_ranges_with_progress_callback(self, mock_isdir):
        """Testaa edistymisen callback-funktion kutsumista mukautetuilla alueilla."""
        ranges = [(1, 2), (4, 6), (8, 8), (10, 10)]
        self.mock_repository.get_page_count.return_value = 10
        mock_callback = MagicMock()
        self.service.split_by_custom_ranges(
            self.test_file_path,
            ranges,
            self.output_dir,
            self.base_filename,
            mock_callback,
        )
        total_parts = len(ranges)
        self.assertEqual(mock_callback.call_count, total_parts)
        mock_callback.assert_called_with(100)

    def test_split_by_custom_ranges_empty_list(self):
        """Testaa virheen käsittelyä, kun annettujen alueiden lista on tyhjä."""
        with self.assertRaisesRegex(
            ValueError, "Vähintään yksi sivualue on määritettävä."
        ):
            self.service.split_by_custom_ranges(
                self.test_file_path, [], self.output_dir
            )

    @patch("os.path.isdir", return_value=True)
    def test_split_by_custom_ranges_invalid_range_format(self, mock_isdir):
        """Testaa virheen käsittelyä, kun alueen muoto on virheellinen."""
        ranges = [(1, 3), "sivu 5", (8, 10)]
        with self.assertRaises(ValueError):
            self.service.split_by_custom_ranges(
                self.test_file_path, ranges, self.output_dir
            )
        self.mock_repository.load_pdf.assert_called_once_with(self.test_file_path)
        self.mock_repository.close_pdf.assert_called_with(self.mock_loaded_doc)

    @patch("os.path.isdir", return_value=True)
    def test_split_by_custom_ranges_range_out_of_bounds(self, mock_isdir):
        """Testaa virheen käsittelyä, kun annettu alue on sivumäärän ulkopuolella."""
        ranges_low = [(0, 3)]
        ranges_high = [(8, 12)]
        self.mock_repository.get_page_count.return_value = 10
        self.mock_repository.load_pdf.return_value = self.mock_loaded_doc

        with self.assertRaisesRegex(
            ValueError, "Virheellinen tai rajojen ulkopuolinen alue: 0-3"
        ):
            self.service.split_by_custom_ranges(
                self.test_file_path, ranges_low, self.output_dir
            )
        self.mock_repository.close_pdf.assert_called_with(self.mock_loaded_doc)

        self.mock_repository.reset_mock()
        self.mock_repository.load_pdf.return_value = self.mock_loaded_doc
        self.mock_repository.get_page_count.return_value = 10

        with self.assertRaisesRegex(
            ValueError, "Virheellinen tai rajojen ulkopuolinen alue: 8-12"
        ):
            self.service.split_by_custom_ranges(
                self.test_file_path, ranges_high, self.output_dir
            )
        self.mock_repository.close_pdf.assert_called_with(self.mock_loaded_doc)

    @patch("os.path.isdir", return_value=True)
    def test_split_by_custom_ranges_start_greater_than_end(self, mock_isdir):
        """Testaa virheen käsittelyä, kun alueen alkusivu on suurempi kuin loppusivu."""
        ranges = [(5, 2)]
        self.mock_repository.get_page_count.return_value = 10
        self.mock_repository.load_pdf.return_value = self.mock_loaded_doc

        with self.assertRaisesRegex(
            ValueError, "Virheellinen tai rajojen ulkopuolinen alue: 5-2"
        ):
            self.service.split_by_custom_ranges(
                self.test_file_path, ranges, self.output_dir
            )
        self.mock_repository.close_pdf.assert_called_with(self.mock_loaded_doc)

    @patch("os.path.isdir", return_value=False)
    def test_split_by_custom_ranges_invalid_output_dir(self, mock_isdir):
        """Testaa virheen käsittelyä mukautetuilla alueilla, kun tulostushakemisto on virheellinen."""
        ranges = [(1, 3)]
        with self.assertRaisesRegex(
            IOError, f"Tulostushakemistoa ei löydy.*: {self.output_dir}"
        ):
            self.service.split_by_custom_ranges(
                self.test_file_path, ranges, self.output_dir
            )
        mock_isdir.assert_called_once_with(self.output_dir)


if __name__ == "__main__":
    unittest.main()
