import os
from src.entities.pdf_document import PDFDocument
from src.repositories.pdf_repository import PDFRepository

class PDFSplitterService:
    """Palveluluokka PDF-tiedostojen jakamiseen
    
    Tarjoaa toiminnallisuuden PDF-tiedostojen jakamiseen useampaan osaan
    joko kiinteän sivumäärän mukaan tai mukautettujen sivualueiden perusteella.
    """
    
    def __init__(self):
        """Alustaa PDF-jakamispalvelun"""
        self.pdf_repository = PDFRepository()
    
    def get_pdf_info(self, file_path):
        """Hakee tiedot PDF-tiedostosta
        
        Args:
            file_path: PDF-tiedoston polku
            
        Returns:
            Sanakirja PDF-tiedoston tiedoista (sivumäärä jne.)
        """
        pdf_document = self.pdf_repository.load_pdf(file_path)
        page_count = self.pdf_repository.get_page_count(pdf_document)
        
        info = {
            "page_count": page_count,
            "file_path": file_path,
            "file_name": os.path.basename(file_path)
        }
        
        self.pdf_repository.close_pdf(pdf_document)
        return info
    
    def split_by_fixed_range(self, file_path, pages_per_file, output_dir=None, base_filename=None):
        """Jakaa PDF-tiedoston osiin, joissa on kiinteä määrä sivuja
        
        Args:
            file_path: PDF-tiedoston polku
            pages_per_file: Sivujen määrä per tiedosto
            output_dir: Hakemisto, johon tulostiedostot tallennetaan (oletus: sama hakemisto)
            base_filename: Tulostiedostojen nimen perusosa (oletus: sama kuin lähdetiedosto)
            
        Returns:
            Lista luotujen tiedostojen poluista
        """
        if pages_per_file < 1:
            raise ValueError("Sivujen määrän per tiedosto tulee olla vähintään 1")
            
        if output_dir is None:
            output_dir = os.path.dirname(file_path)
            
        if base_filename is None:
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        pdf_document = self.pdf_repository.load_pdf(file_path)
        page_count = self.pdf_repository.get_page_count(pdf_document)
        
        output_files = []
        
        for i in range(0, page_count, pages_per_file):
            start_page = i
            end_page = min(i + pages_per_file - 1, page_count - 1)
            
            new_doc = self.pdf_repository.extract_pages(pdf_document, start_page, end_page)
            
            output_filename = f"{base_filename}_sivut_{start_page+1}-{end_page+1}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            self.pdf_repository.save_pdf(new_doc, output_path)
            output_files.append(output_path)
            
            self.pdf_repository.close_pdf(new_doc)
        
        self.pdf_repository.close_pdf(pdf_document)
        
        return output_files
    
    def split_by_custom_ranges(self, file_path, ranges, output_dir=None, base_filename=None):
        """Jakaa PDF-tiedoston osiin mukautettujen sivualueiden mukaan
        
        Args:
            file_path: PDF-tiedoston polku
            ranges: Lista tupleja (alku, loppu), joissa alku ja loppu ovat sivunumeroita (1-pohjaisia)
            output_dir: Hakemisto, johon tulostiedostot tallennetaan (oletus: sama hakemisto)
            base_filename: Tulostiedostojen nimen perusosa (oletus: sama kuin lähdetiedosto)
            
        Returns:
            Lista luotujen tiedostojen poluista
        """
        if not ranges:
            raise ValueError("Vähintään yksi sivualue on määritettävä")
            
        if output_dir is None:
            output_dir = os.path.dirname(file_path)
            
        if base_filename is None:
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
        
        pdf_document = self.pdf_repository.load_pdf(file_path)
        page_count = self.pdf_repository.get_page_count(pdf_document)
        
        output_files = []
        
        for i, (start, end) in enumerate(ranges):
            zero_based_start = start - 1
            zero_based_end = end - 1
            
            if zero_based_start < 0:
                zero_based_start = 0
            if zero_based_end >= page_count:
                zero_based_end = page_count - 1
            if zero_based_start > zero_based_end:
                zero_based_start, zero_based_end = zero_based_end, zero_based_start
            
            new_doc = self.pdf_repository.extract_pages(
                pdf_document, zero_based_start, zero_based_end
            )
            
            output_filename = f"{base_filename}_alue_{i+1}_sivut_{start}-{end}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            self.pdf_repository.save_pdf(new_doc, output_path)
            output_files.append(output_path)
            
            self.pdf_repository.close_pdf(new_doc)
        
        self.pdf_repository.close_pdf(pdf_document)
        
        return output_files