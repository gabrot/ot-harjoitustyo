class PDFDocument:
    """Luokka, joka kuvaa PDF-dokumenttia
    
    Attributes:
        file_path: PDF-tiedoston polku
        page_count: PDF-tiedoston sivujen määrä
    """
    
    def __init__(self, file_path, page_count):
        """Alustaa uuden PDF-dokumentin
        
        Args:
            file_path: Tiedoston polku
            page_count: Sivujen määrä
        """
        self.file_path = file_path
        self.page_count = page_count