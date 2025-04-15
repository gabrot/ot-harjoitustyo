import unittest
from ..entities.pdf_document import PDFDocument


class TestPDFDocument(unittest.TestCase):
    """Testiluokka PDFDocument-luokan perustoiminnallisuuden testaamiseen.

    Varmistaa, että luokan konstruktori alustaa olion attribuutit
    (tiedostopolku ja sivumäärä) oikein annetuilla arvoilla.
    """

    def test_constructor_sets_attributes_correctly(self):
        """Testaa, että konstruktori asettaa tiedostopolun ja sivumäärän oikein.

        Tämä testi luo PDFDocument-olion tietyillä syötteillä ja tarkistaa,
        että olion 'file_path' ja 'page_count' -attribuutit vastaavat
        annettuja arvoja. Testi varmistaa luokan perusdatan säilömisen.
        """
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
