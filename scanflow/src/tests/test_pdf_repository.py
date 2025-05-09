from src.repositories.pdf_repository import PDFRepository
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import fitz

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_data")
EMPTY_PDF = os.path.join(TEST_DATA_DIR, "empty.pdf")
FAKE_PDF = os.path.join(TEST_DATA_DIR, "fake.pdf")
BROKEN_PDF = os.path.join(TEST_DATA_DIR, "broken.pdf")
CORRUPT_TRUNCATED_PDF = os.path.join(TEST_DATA_DIR, "corrupt_truncated.pdf")


class TestPDFRepository(unittest.TestCase):

    def setUp(self):
        self.repository = PDFRepository()
        self.test_file_path = os.path.join("dummy", "test_document.pdf")
        self.mock_doc = MagicMock()
        self.mock_doc.is_closed = False
        self.mock_doc.is_pdf = True
        self.mock_doc.page_count = 10
        self.mock_doc.metadata = None

    @patch("os.path.exists")
    @patch("fitz.open")
    def test_load_pdf_success(self, mock_fitz_open, mock_os_exists):
        mock_os_exists.return_value = True
        mock_fitz_open.return_value = self.mock_doc

        result = self.repository.load_pdf(self.test_file_path)

        mock_os_exists.assert_called_once_with(self.test_file_path)
        mock_fitz_open.assert_called_once_with(self.test_file_path)
        self.assertIs(result, self.mock_doc)
        self.assertTrue(result.is_pdf)
        self.assertFalse(result.is_closed)
        result.close.assert_not_called()

    @patch("os.path.exists")
    def test_load_pdf_file_not_found(self, mock_os_exists):
        mock_os_exists.return_value = False
        with self.assertRaisesRegex(FileNotFoundError, "Tiedostoa ei löydy"):
            self.repository.load_pdf(self.test_file_path)
        mock_os_exists.assert_called_once_with(self.test_file_path)

    @patch("os.path.exists")
    @patch("fitz.open")
    def test_load_pdf_not_valid_pdf(self, mock_fitz_open, mock_os_exists):
        mock_os_exists.return_value = True
        invalid_mock_doc = MagicMock()
        invalid_mock_doc.is_pdf = False
        invalid_mock_doc.close = MagicMock()
        mock_fitz_open.return_value = invalid_mock_doc

        with self.assertRaisesRegex(ValueError, "Tiedosto ei ole kelvollinen PDF"):
            self.repository.load_pdf(self.test_file_path)

        mock_os_exists.assert_called_once_with(self.test_file_path)
        mock_fitz_open.assert_called_once_with(self.test_file_path)
        invalid_mock_doc.close.assert_called_once()

    @patch("os.path.exists")
    @patch("fitz.open", side_effect=Exception("Test exception"))
    def test_load_pdf_open_exception(self, mock_fitz_open, mock_os_exists):
        mock_os_exists.return_value = True
        with self.assertRaisesRegex(
            ValueError, "avaaminen epäonnistui: Test exception"
        ):
            self.repository.load_pdf(self.test_file_path)
        mock_os_exists.assert_called_once_with(self.test_file_path)
        mock_fitz_open.assert_called_once_with(self.test_file_path)

    @patch("os.path.exists", return_value=True)
    @patch("fitz.open", side_effect=Exception("cannot open empty file"))
    def test_load_pdf_empty_file(self, mock_fitz_open, mock_os_exists):
        with self.assertRaisesRegex(
            ValueError, "avaaminen epäonnistui: cannot open empty file"
        ):
            self.repository.load_pdf(EMPTY_PDF)
        mock_os_exists.assert_called_once_with(EMPTY_PDF)
        mock_fitz_open.assert_called_once_with(EMPTY_PDF)

    @patch("os.path.exists", return_value=True)
    @patch("fitz.open", side_effect=Exception("not a PDF"))
    def test_load_pdf_non_pdf_content(self, mock_fitz_open, mock_os_exists):
        """Test loading a file with non-PDF text content."""
        with self.assertRaisesRegex(ValueError, "avaaminen epäonnistui: not a PDF"):
            self.repository.load_pdf(FAKE_PDF)
        mock_os_exists.assert_called_once_with(FAKE_PDF)
        mock_fitz_open.assert_called_once_with(FAKE_PDF)

    @patch("os.path.exists", return_value=True)
    @patch("fitz.open", side_effect=Exception("syntax error"))
    def test_load_pdf_broken_content(self, mock_fitz_open, mock_os_exists):
        with self.assertRaisesRegex(ValueError, "avaaminen epäonnistui: syntax error"):
            self.repository.load_pdf(BROKEN_PDF)
        mock_os_exists.assert_called_once_with(BROKEN_PDF)
        mock_fitz_open.assert_called_once_with(BROKEN_PDF)

    @patch("os.path.exists", return_value=True)
    @patch("fitz.open", side_effect=Exception("premature end-of-file"))
    def test_load_pdf_corrupt_truncated(self, mock_fitz_open, mock_os_exists):
        with self.assertRaisesRegex(
            ValueError, "avaaminen epäonnistui: premature end-of-file"
        ):
            self.repository.load_pdf(CORRUPT_TRUNCATED_PDF)
        mock_os_exists.assert_called_once_with(CORRUPT_TRUNCATED_PDF)
        mock_fitz_open.assert_called_once_with(CORRUPT_TRUNCATED_PDF)

    def test_get_page_count_success(self):
        self.mock_doc.page_count = 15
        result = self.repository.get_page_count(self.mock_doc)
        self.assertEqual(result, 15)

    def test_get_page_count_closed_document(self):
        self.mock_doc.is_closed = True
        with self.assertRaisesRegex(ValueError, "Dokumentti on suljettu."):
            self.repository.get_page_count(self.mock_doc)

    def test_get_metadata_success(self):
        test_metadata = {"title": "Test Title", "author": "Test Author"}
        self.mock_doc.metadata = test_metadata
        result = self.repository.get_metadata(self.mock_doc)
        self.assertEqual(result, test_metadata)

    def test_get_metadata_empty(self):
        self.mock_doc.metadata = None
        result = self.repository.get_metadata(self.mock_doc)
        self.assertEqual(result, {})

    def test_get_metadata_closed_document(self):
        self.mock_doc.is_closed = True
        with self.assertRaisesRegex(ValueError, "Dokumentti on suljettu."):
            self.repository.get_metadata(self.mock_doc)

    @patch("fitz.open")
    def test_extract_pages_success(self, mock_fitz_open_new):
        mock_new_doc = MagicMock()
        mock_new_doc.insert_pdf = MagicMock()
        mock_fitz_open_new.return_value = mock_new_doc
        self.mock_doc.page_count = 10

        result = self.repository.extract_pages(self.mock_doc, 2, 5)

        mock_fitz_open_new.assert_called_once()
        mock_new_doc.insert_pdf.assert_called_once_with(
            self.mock_doc, from_page=2, to_page=5
        )
        self.assertIs(result, mock_new_doc)

    @patch("fitz.open")
    def test_extract_pages_invalid_range_returns_empty(self, mock_fitz_open_new):
        mock_empty_doc = MagicMock()
        mock_empty_doc.insert_pdf = MagicMock()
        mock_fitz_open_new.return_value = mock_empty_doc
        self.mock_doc.page_count = 10

        result = self.repository.extract_pages(self.mock_doc, 5, 2)

        mock_fitz_open_new.assert_called_once()
        mock_empty_doc.insert_pdf.assert_not_called()
        self.assertIs(result, mock_empty_doc)

    @patch("fitz.open")
    def test_extract_pages_clamps_indices(self, mock_fitz_open_new):
        mock_new_doc = MagicMock()
        mock_new_doc.insert_pdf = MagicMock()
        mock_fitz_open_new.return_value = mock_new_doc
        self.mock_doc.page_count = 5

        self.repository.extract_pages(self.mock_doc, -2, 3)
        mock_new_doc.insert_pdf.assert_called_with(
            self.mock_doc, from_page=0, to_page=3
        )

        mock_new_doc.insert_pdf.reset_mock()
        self.repository.extract_pages(self.mock_doc, 1, 10)
        mock_new_doc.insert_pdf.assert_called_with(
            self.mock_doc, from_page=1, to_page=4
        )

        mock_new_doc.insert_pdf.reset_mock()
        self.repository.extract_pages(self.mock_doc, -1, 7)
        mock_new_doc.insert_pdf.assert_called_with(
            self.mock_doc, from_page=0, to_page=4
        )

    def test_extract_pages_closed_document(self):
        self.mock_doc.is_closed = True
        with self.assertRaisesRegex(ValueError, "Alkuperäinen dokumentti on suljettu."):
            self.repository.extract_pages(self.mock_doc, 0, 1)

    @patch("fitz.open")
    def test_extract_pages_insert_exception(self, mock_fitz_open_new):
        mock_new_doc = MagicMock()
        mock_new_doc.insert_pdf = MagicMock(side_effect=Exception("Insert failed"))
        mock_new_doc.close = MagicMock()
        mock_fitz_open_new.return_value = mock_new_doc
        self.mock_doc.page_count = 10

        with self.assertRaisesRegex(ValueError, "poiminta epäonnistui: Insert failed"):
            self.repository.extract_pages(self.mock_doc, 1, 3)

        mock_new_doc.close.assert_called_once()

    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("os.path.dirname")
    def test_save_pdf_success(self, mock_dirname, mock_exists, mock_makedirs):
        output_path = os.path.join("output", "test_output.pdf")
        mock_dirname.return_value = "output"
        mock_exists.return_value = True

        self.mock_doc.save = MagicMock()

        result = self.repository.save_pdf(self.mock_doc, output_path)

        mock_dirname.assert_called_once_with(output_path)
        mock_exists.assert_called_once_with("output")
        mock_makedirs.assert_not_called()
        self.mock_doc.save.assert_called_once_with(output_path, garbage=4, deflate=True)
        self.assertEqual(result, output_path)

    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("os.path.dirname")
    def test_save_pdf_creates_directory(self, mock_dirname, mock_exists, mock_makedirs):
        output_path = os.path.join("new_output", "subdir", "test_output.pdf")
        output_dir = os.path.join("new_output", "subdir")
        mock_dirname.return_value = output_dir
        mock_exists.return_value = False

        self.mock_doc.save = MagicMock()

        self.repository.save_pdf(self.mock_doc, output_path)

        mock_dirname.assert_called_once_with(output_path)
        mock_exists.assert_called_once_with(output_dir)
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        self.mock_doc.save.assert_called_once_with(output_path, garbage=4, deflate=True)

    def test_save_pdf_closed_document(self):
        self.mock_doc.is_closed = True
        output_path = os.path.join("output", "test_output.pdf")
        with self.assertRaisesRegex(
            ValueError, "Tallennettava dokumentti on suljettu."
        ):
            self.repository.save_pdf(self.mock_doc, output_path)

    @patch("os.makedirs", side_effect=OSError("Permission denied"))
    @patch("os.path.exists", return_value=False)
    @patch("os.path.dirname")
    def test_save_pdf_makedirs_oserror(self, mock_dirname, mock_exists, mock_makedirs):
        output_path = os.path.join("restricted_dir", "test.pdf")
        output_dir = "restricted_dir"
        mock_dirname.return_value = output_dir
        self.mock_doc.save = MagicMock()

        with self.assertRaisesRegex(
            IOError,
            f"Kohdehakemiston '{output_dir}' luominen epäonnistui: Permission denied",
        ):
            self.repository.save_pdf(self.mock_doc, output_path)

        self.mock_doc.save.assert_not_called()

    @patch("os.path.exists", return_value=True)
    @patch("os.path.dirname")
    def test_save_pdf_save_exception(self, mock_dirname, mock_exists):
        output_path = os.path.join("output", "fail.pdf")
        mock_dirname.return_value = "output"
        self.mock_doc.save = MagicMock(side_effect=Exception("Disk full"))

        with self.assertRaisesRegex(
            Exception, "PDF-dokumentin tallennus.*epäonnistui: Disk full"
        ):
            self.repository.save_pdf(self.mock_doc, output_path)
        self.mock_doc.save.assert_called_once_with(output_path, garbage=4, deflate=True)

    def test_close_pdf_success(self):
        self.mock_doc.is_closed = False
        self.mock_doc.close = MagicMock()

        self.repository.close_pdf(self.mock_doc)

        self.mock_doc.close.assert_called_once()

    def test_close_pdf_already_closed(self):
        self.mock_doc.is_closed = True
        self.mock_doc.close = MagicMock()
        self.repository.close_pdf(self.mock_doc)

        self.mock_doc.close.assert_not_called()

    def test_close_pdf_none_document(self):
        try:
            self.repository.close_pdf(None)
        except Exception as e:
            self.fail(f"close_pdf(None) nosti odottamattoman poikkeuksen: {e}")

    def test_close_pdf_exception_suppressed(self):
        self.mock_doc.is_closed = False
        self.mock_doc.close = MagicMock(side_effect=Exception("Internal close error"))

        with self.assertRaises(Exception) as context:
            self.repository.close_pdf(self.mock_doc)

        self.assertEqual(str(context.exception), "Internal close error")
        self.mock_doc.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
