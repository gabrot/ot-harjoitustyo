"""Apufunktioita Scanflow-sovellukselle."""

import os
from PIL import Image, ImageTk

def get_file_size_str(size_bytes):
    """Muuntaa tavut ihmisluettavaksi kooksi.
    
    Args:
        size_bytes: Koko tavuina
        
    Returns:
        Merkkijono, joka kuvaa kokoa (esim. "1.5 MB")
    """
    units = ["B", "KB", "MB", "GB", "TB"]
    
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"

def create_pdf_preview(pdf_doc, page_index=0, width=300):
    """Luo esikatselukuvan PDF-sivusta.
    
    Args:
        pdf_doc: PyMuPDF-dokumenttiolio
        page_index: Sivun indeksi (0-pohjainen)
        width: Haluttu leveys pikseleinä
        
    Returns:
        ImageTk.PhotoImage-olio
    """
    if pdf_doc is None or pdf_doc.page_count <= page_index:
        return None
    
    try:
        page = pdf_doc[page_index]
        
        pix = page.get_pixmap()
        
        img_data = pix.samples
        img_mode = "RGB" if pix.n == 3 else "RGBA"
        img = Image.frombytes(img_mode, [pix.width, pix.height], img_data)
        
        wpercent = (width/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((width, hsize), Image.LANCZOS)
        
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Virhe esikatselukuvan luomisessa: {e}")
        return None

def validate_parts_count(value):
    """Tarkistaa, että annettu arvo on kokonaisluku välillä 1-100.
    
    Args:
        value: Tarkistettava arvo
        
    Returns:
        True jos arvo on kelvollinen, muuten False
    """
    if value == "":
        return True
    
    try:
        num = int(value)
        return 1 <= num <= 100
    except ValueError:
        return False

def parse_page_ranges(text, max_pages):
    """Jäsentää sivualueet tekstistä.
    
    Args:
        text: Tekstimuotoinen sivualueiden kuvaus (esim. "1-5, 8, 11-13")
        max_pages: Suurin sallittu sivunumero
        
    Returns:
        Lista sivualueita muodossa [(alku, loppu), ...] tai None jos virhe
    """
    try:
        parts = text.split(",")
        ranges = []
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            if "-" in part:
                start, end = part.split("-")
                start = int(start.strip())
                end = int(end.strip())
                
                if start < 1 or end > max_pages or start > end:
                    raise ValueError(f"Virheellinen sivualue: {part}")
                
                ranges.append((start, end))
            else:
                page = int(part)
                
                if page < 1 or page > max_pages:
                    raise ValueError(f"Virheellinen sivu: {part}")
                
                ranges.append((page, page))
        
        return ranges
    except Exception as e:
        print(f"Virhe sivualueiden jäsentämisessä: {e}")
        return None