import unittest
from ..entities.pdf_document import PDFDocument


class TestPDFDocument(unittest.TestCase):

    def test_constructor_sets_attributes_correctly(self):

        file_path = "/polku/dokumentti.pdf"
        page_count = 10

        document = PDFDocument(file_path, page_count)

        self.assertEqual(
            document.file_path, file_path, "Tiedostopolku ei vastaa annettua."
        )
        self.assertEqual(
            document.page_count, page_count, "Sivumäärä ei vastaa annettua."
        )


if __name__ == "__main__":
    unittest.main()
