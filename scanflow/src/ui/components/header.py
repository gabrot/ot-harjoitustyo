import tkinter as tk
from tkinter import ttk
from ui.theme import ThemeFonts, ThemeColors

class Header(ttk.Frame):
    """Sovelluksen ylätunniste komponentti"""
    
    def __init__(self, parent, title="PDF-jakaja", subtitle=None):
        """Alustaa ylätunnisteen
        
        Args:
            parent: Vanhempi elementti
            title: Otsikkoteksti
            subtitle: Alaotsikko (valinnainen)
        """
        super().__init__(parent, style="Header.TFrame")
        
        title_label = ttk.Label(
            self, 
            text=title,
            style="HeaderTitle.TLabel"
        )
        title_label.pack(anchor="w", pady=(0, 5))
        
        if subtitle:
            subtitle_label = ttk.Label(
                self, 
                text=subtitle,
                style="HeaderSubtitle.TLabel"
            )
            subtitle_label.pack(anchor="w")
            
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill=tk.X, pady=(10, 0))