import tkinter as tk
from tkinter import ttk, filedialog
import os
from ui.theme import ThemeColors, ThemeFonts


class DropArea(ttk.Frame):
    """Tiedoston pudotusalue komponentti
    
    Mahdollistaa tiedoston valinnan raahaamalla tai valintaikkunan kautta.
    """
    
    def __init__(self, parent, on_file_selected):
        """Alustaa tiedoston pudotusalueen
        
        Args:
            parent: Vanhempi elementti
            on_file_selected: Funktio, jota kutsutaan kun tiedosto on valittu
        """
        super().__init__(
            parent,
            style="DropArea.TFrame"
        )
        
        self.parent = parent
        self.on_file_selected = on_file_selected
        
        self._create_widgets()
        self._setup_drop_bindings()
    
    def _create_widgets(self):
        """Luo tarvittavat käyttöliittymäelementit"""
        self.configure(height=120, style="DropArea.TFrame")
        
        text_frame = ttk.Frame(self, style="DropText.TFrame")
        text_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        instruction_label = ttk.Label(
            text_frame,
            text="Raahaa PDF-tiedosto tähän",
            style="DropText.TLabel"
        )
        instruction_label.pack(pady=5)
        
        or_label = ttk.Label(
            text_frame,
            text="- tai -",
            style="DropTextSecondary.TLabel"
        )
        or_label.pack(pady=5)
        
        browse_button = ttk.Button(
            text_frame,
            text="Valitse tiedosto",
            command=self._browse_file,
            style="Browse.TButton"
        )
        browse_button.pack(pady=5)
    
    def _setup_drop_bindings(self):
        """Asettaa tiedoston pudotukseen liittyvät tapahtumasidokset"""
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonRelease-1>", self._on_click)
        
    def _on_enter(self, event):
        """Hiiren tullessa alueen päälle"""
        self.configure(style="DropAreaHover.TFrame")
        
    def _on_leave(self, event):
        """Hiiren poistuessa alueelta"""
        self.configure(style="DropArea.TFrame")
        
    def _on_click(self, event):
        """Hiiren klikkaus alueella"""
        self._browse_file()
        
    def _browse_file(self):
        """Avaa tiedoston valintaikkunan"""
        file_path = filedialog.askopenfilename(
            title="Valitse PDF-tiedosto",
            filetypes=[("PDF tiedostot", "*.pdf")]
        )
        
        if file_path:
            self.on_file_selected(file_path)