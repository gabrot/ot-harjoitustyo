import os
import fitz  # PyMuPDF

class PDFRepository:
    """Repository-luokka PDF-tiedostojen käsittelyyn
    
    Luokka vastaa PDF-tiedostojen lataamisesta, tallentamisesta
    ja manipuloinnista PyMuPDF-kirjaston avulla.
    """
    
    def load_pdf(self, file_path):
        """Lataa PDF-tiedoston ja palauttaa dokumenttiolion
        
        Args:
            file_path: Polku PDF-tiedostoon
            
        Returns:
            PyMuPDF-dokumenttiolio
            
        Raises:
            FileNotFoundError: Jos tiedostoa ei löydy
            ValueError: Jos tiedosto ei ole kelvollinen PDF
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Tiedostoa ei löydy: {file_path}")
        
        try:
            return fitz.open(file_path)
        except Exception as e:
            raise ValueError(f"PDF-tiedoston avaus epäonnistui: {e}")
    
    def get_page_count(self, pdf_document):
        """Palauttaa PDF-dokumentin sivujen määrän
        
        Args:
            pdf_document: PyMuPDF-dokumenttiolio
            
        Returns:
            Sivujen lukumäärä kokonaislukuna
        """
        return pdf_document.page_count
    
    def extract_pages(self, pdf_document, start_page, end_page):
        """Poimii määritetyt sivut PDF-dokumentista
        
        Args:
            pdf_document: PyMuPDF-dokumenttiolio
            start_page: Aloitussivu (0-pohjainen indeksi)
            end_page: Lopetussivu (0-pohjainen indeksi, sisältyy)
            
        Returns:
            Uusi PyMuPDF-dokumentti, joka sisältää määritetyt sivut
        """
        new_doc = fitz.open()
        new_doc.insert_pdf(pdf_document, from_page=start_page, to_page=end_page)
        return new_doc
    
    def save_pdf(self, pdf_document, output_path):
        """Tallentaa PDF-dokumentin määritettyyn polkuun
        
        Args:
            pdf_document: PyMuPDF-dokumenttiolio
            output_path: Polku, johon dokumentti tallennetaan
            
        Returns:
            Polku, johon dokumentti tallennettiin
        """
        pdf_document.save(output_path)
        return output_path
    
    def close_pdf(self, pdf_document):
        """Sulkee PDF-dokumentin
        
        Args:
            pdf_document: PyMuPDF-dokumenttiolio
        """
        pdf_document.close()