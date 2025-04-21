"""
Moduuli PDF-dokumenttien datamallille sovelluksessa.

Tämä moduuli sisältää `PDFDocument`-luokan, joka edustaa yksinkertaista
datarakennetta ladatulle PDF-tiedostolle.
"""


class PDFDocument:
    """
    Yksinkertainen luokka kuvaamaan ladattua PDF-dokumenttia.

    Säilöö perustiedot PDF-tiedostosta, kuten sen tiedostopolun ja
    kokonaissivumäärän.

    Attributes:
        file_path (str): PDF-tiedoston täydellinen polku levyltä.
        page_count (int): PDF-tiedoston sivujen kokonaismäärä.
    """

    def __init__(self, file_path: str, page_count: int):
        """
        Alustaa uuden PDFDocument-olion.

        Args:
            file_path: Ladatun PDF-tiedoston polku.
            page_count: Ladatun PDF-tiedoston sivumäärä.
        """
        self.file_path = file_path
        self.page_count = page_count

    def __repr__(self):
        """
        Palauttaa merkkijonoesityksen PDFDocument-oliosta.

        Returns:
            str: Merkkijonoesitys, joka sisältää tiedostopolun ja sivumäärän.
        """
        return f"PDFDocument(file_path='{self.file_path}', page_count={self.page_count})"
