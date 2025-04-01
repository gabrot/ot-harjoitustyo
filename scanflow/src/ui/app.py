import tkinter as tk
from tkinter import ttk, filedialog
import os
from PIL import Image, ImageTk

from services.pdf_splitter_service import PDFSplitterService
from ui.components.drop_area import DropArea
from ui.theme import ThemeColors, ThemeFonts


class PdfSplitterApp:
    def __init__(self, root):
        """PDF-jakaja sovelluksen päänäkymä

        Args:
            root: Tkinter-ikkunan juuri
        """
        self.root = root
        self.pdf_service = PDFSplitterService()
        self.current_file_path = None
        self.current_pdf = None
        self.page_count = 0
        
        self.range_mode = tk.StringVar(value="fixed")  # "fixed" tai "custom"
        self.fixed_pages_count = tk.StringVar(value="2")
        self.custom_ranges = []  # Lista (alku, loppu) -tupleista
        
        self._init_ui()
    
    def _init_ui(self):
        """Alustaa käyttöliittymän peruskomponentit"""
        self.root.title("PDF-jakaja")
        self.root.configure(bg=ThemeColors.BACKGROUND)
        self.root.geometry("600x650")
        self.root.minsize(500, 600)
        
        # Pääkontaineri
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Otsikko
        title_label = ttk.Label(
            main_frame, 
            text="PDF-jakaja",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))
        
        # Tiedoston pudotusalue
        self.drop_area = DropArea(main_frame, self._on_file_selected)
        self.drop_area.pack(fill=tk.X, pady=10)
        
        # Tiedoston tiedot
        self.file_info_frame = ttk.Frame(main_frame, style="InfoFrame.TFrame")
        self.file_info_frame.pack(fill=tk.X, pady=10)
        
        self.file_name_label = ttk.Label(
            self.file_info_frame, 
            text="", 
            style="FileInfo.TLabel"
        )
        self.file_name_label.pack(anchor="w", pady=5)
        
        self.page_info_label = ttk.Label(
            self.file_info_frame, 
            text="", 
            style="FileInfo.TLabel"
        )
        self.page_info_label.pack(anchor="w", pady=5)
        
        # Asetustilan valinta
        self._create_range_mode_selector(main_frame)
        
        # Alueet kehys
        self.ranges_frame = ttk.Frame(main_frame, style="RangesFrame.TFrame")
        self.ranges_frame.pack(fill=tk.X, pady=10)
        
        # Kiinteät alueet näkymä
        self.fixed_ranges_frame = ttk.Frame(self.ranges_frame, style="Main.TFrame")
        
        # Mukautetut alueet näkymä
        self.custom_ranges_frame = ttk.Frame(self.ranges_frame, style="Main.TFrame")
        
        # Tulostusasetukset
        self.output_frame = ttk.Frame(main_frame, style="Main.TFrame")
        self.output_frame.pack(fill=tk.X, pady=20)
        
        # Jakamispainike
        self.split_button = ttk.Button(
            main_frame,
            text="Jaa PDF",
            command=self._split_pdf,
            style="Action.TButton"
        )
        self.split_button.pack(pady=20)
        self.split_button.config(state=tk.DISABLED)
        
        # Statusalue
        self.status_frame = ttk.Frame(main_frame, style="StatusFrame.TFrame")
        self.status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="", 
            style="Status.TLabel"
        )
        self.status_label.pack(pady=5)
        
        # Näytetään kiinteät alueet oletuksena
        self._create_fixed_ranges_view()
        self._create_custom_ranges_view()
        self._update_range_view()
    
    def _create_range_mode_selector(self, parent):
        """Luo asetustilan valitsimen

        Args:
            parent: Vanhempi elementti
        """
        mode_frame = ttk.Frame(parent, style="ModeSelector.TFrame")
        mode_frame.pack(fill=tk.X, pady=15)
        
        mode_label = ttk.Label(
            mode_frame, 
            text="Asetustila:", 
            style="ModeLabel.TLabel"
        )
        mode_label.pack(anchor="w", pady=(0, 10))
        
        button_frame = ttk.Frame(mode_frame)
        button_frame.pack(fill=tk.X)
        
        # Omat alueet -painike
        self.custom_button = ttk.Button(
            button_frame,
            text="Omat alueet",
            command=lambda: self._change_range_mode("custom"),
            style="ModeButton.TButton" if self.range_mode.get() != "custom" else "ModeButtonActive.TButton",
            width=15
        )
        self.custom_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Kiinteät alueet -painike
        self.fixed_button = ttk.Button(
            button_frame,
            text="Kiinteät alueet",
            command=lambda: self._change_range_mode("fixed"),
            style="ModeButtonActive.TButton" if self.range_mode.get() == "fixed" else "ModeButton.TButton",
            width=15
        )
        self.fixed_button.pack(side=tk.LEFT)
    
    def _create_fixed_ranges_view(self):
        """Luo kiinteiden alueiden näkymän"""
        for widget in self.fixed_ranges_frame.winfo_children():
            widget.destroy()
        
        # Sivumäärä kentän otsikko
        pages_label = ttk.Label(
            self.fixed_ranges_frame, 
            text="Jaa PDF sivualueisiin, joiden koko on:",
            style="RangeLabel.TLabel"
        )
        pages_label.pack(anchor="w", pady=(0, 10))
        
        # Sivumäärän valitsin
        pages_frame = ttk.Frame(self.fixed_ranges_frame)
        pages_frame.pack(fill=tk.X, pady=5)
        
        pages_spinbox = ttk.Spinbox(
            pages_frame,
            from_=1,
            to=100,
            textvariable=self.fixed_pages_count,
            width=5,
            wrap=True
        )
        pages_spinbox.pack(side=tk.RIGHT)
        
        # Infoteksti
        self.fixed_info_frame = ttk.Frame(self.fixed_ranges_frame, style="InfoBox.TFrame")
        self.fixed_info_frame.pack(fill=tk.X, pady=15)
        
        self.fixed_info_label = ttk.Label(
            self.fixed_info_frame,
            text="",
            style="InfoText.TLabel",
            wraplength=500
        )
        self.fixed_info_label.pack(pady=15, padx=15)
        
        # Päivitä info jos tiedosto on valittu
        self._update_fixed_info()
    
    def _create_custom_ranges_view(self):
        """Luo mukautettujen alueiden näkymän"""
        for widget in self.custom_ranges_frame.winfo_children():
            widget.destroy()
            
        # Jos mukautettuja alueita ei ole, lisätään ensimmäinen
        if not self.custom_ranges:
            self._add_custom_range(1, self.page_count if self.page_count > 0 else 1)
        
        # Lisää olemassa olevat alueet näkymään
        range_index = 0
        for start, end in self.custom_ranges:
            self._create_custom_range_row(range_index, start, end)
            range_index += 1
        
        # Lisää uusi alue -painike
        add_button = ttk.Button(
            self.custom_ranges_frame,
            text="+ Lisää alue",
            command=self._add_new_range,
            style="AddRange.TButton"
        )
        add_button.pack(pady=15)
    
    def _create_custom_range_row(self, index, start_value, end_value):
        """Luo yksittäisen mukautetun alueen rivin

        Args:
            index: Alueen indeksi
            start_value: Alkusivu
            end_value: Loppusivu
        """
        # Pääkehys tälle alueelle
        range_frame = ttk.Frame(self.custom_ranges_frame)
        range_frame.pack(fill=tk.X, pady=5)
        
        # Indeksin näyttö
        index_frame = ttk.Frame(range_frame)
        index_frame.pack(fill=tk.X, pady=2)
        
        index_label = ttk.Label(
            index_frame,
            text=f"Alue {index+1}",
            style="RangeIndex.TLabel"
        )
        index_label.pack(side=tk.LEFT)
        
        # Poistopainike
        if len(self.custom_ranges) > 1:
            delete_button = ttk.Button(
                index_frame,
                text="×",
                command=lambda i=index: self._delete_range(i),
                width=2,
                style="DeleteRange.TButton"
            )
            delete_button.pack(side=tk.RIGHT)
        
        # Alkusivu
        start_frame = ttk.Frame(range_frame)
        start_frame.pack(fill=tk.X, pady=2)
        
        start_label = ttk.Label(
            start_frame,
            text="alkaen sivulta",
            style="RangeLabel.TLabel",
            width=15
        )
        start_label.pack(side=tk.LEFT)
        
        # Sivujen lukumäärä tälle alueelle
        start_var = tk.StringVar(value=str(start_value))
        start_spinbox = ttk.Spinbox(
            start_frame,
            from_=1,
            to=self.page_count if self.page_count > 0 else 100,
            textvariable=start_var,
            width=8,
            command=lambda: self._update_range_value(index, "start", start_var.get())
        )
        start_spinbox.pack(side=tk.RIGHT)
        start_spinbox.bind("<FocusOut>", lambda e, i=index, v=start_var: 
                           self._update_range_value(i, "start", v.get()))
        
        # Loppusivu
        end_frame = ttk.Frame(range_frame)
        end_frame.pack(fill=tk.X, pady=2)
        
        end_label = ttk.Label(
            end_frame,
            text="sivulle",
            style="RangeLabel.TLabel",
            width=15
        )
        end_label.pack(side=tk.LEFT)
        
        # Loppusivun valitsin
        end_var = tk.StringVar(value=str(end_value))
        end_spinbox = ttk.Spinbox(
            end_frame,
            from_=1,
            to=self.page_count if self.page_count > 0 else 100,
            textvariable=end_var,
            width=8,
            command=lambda: self._update_range_value(index, "end", end_var.get())
        )
        end_spinbox.pack(side=tk.RIGHT)
        end_spinbox.bind("<FocusOut>", lambda e, i=index, v=end_var: 
                         self._update_range_value(i, "end", v.get()))
        
        # Näytä erotin, jos ei ole viimeinen
        if index < len(self.custom_ranges) - 1:
            separator = ttk.Separator(self.custom_ranges_frame, orient="horizontal")
            separator.pack(fill=tk.X, pady=10)
    
    def _update_range_value(self, index, field, value):
        """Päivittää mukautetun alueen arvon

        Args:
            index: Alueen indeksi
            field: Kenttä (start/end)
            value: Uusi arvo
        """
        try:
            value = int(value)
            if value < 1:
                value = 1
            if self.page_count > 0 and value > self.page_count:
                value = self.page_count
                
            if index < len(self.custom_ranges):
                start, end = self.custom_ranges[index]
                
                if field == "start":
                    value = min(value, end)
                    self.custom_ranges[index] = (value, end)
                else:
                    value = max(value, start)
                    self.custom_ranges[index] = (start, value)
                
                self._create_custom_ranges_view()
        except ValueError:
            self._create_custom_ranges_view()
    
    def _add_new_range(self):
        """Lisää uuden mukautetun alueen"""
        if self.page_count > 0:
            self._add_custom_range(self.page_count, self.page_count)
        else:
            self._add_custom_range(1, 1)
        self._create_custom_ranges_view()
    
    def _add_custom_range(self, start, end):
        """Lisää uuden mukautetun alueen annetuilla arvoilla

        Args:
            start: Aloitussivu
            end: Lopetussivu
        """
        self.custom_ranges.append((start, end))
    
    def _delete_range(self, index):
        """Poistaa mukautetun alueen

        Args:
            index: Poistettavan alueen indeksi
        """
        if 0 <= index < len(self.custom_ranges) and len(self.custom_ranges) > 1:
            del self.custom_ranges[index]
            self._create_custom_ranges_view()
    
    def _change_range_mode(self, mode):
        """Vaihtaa asetustilaa

        Args:
            mode: Uusi tila (fixed/custom)
        """
        self.range_mode.set(mode)
        
        self.custom_button.configure(
            style="ModeButtonActive.TButton" if mode == "custom" else "ModeButton.TButton"
        )
        self.fixed_button.configure(
            style="ModeButtonActive.TButton" if mode == "fixed" else "ModeButton.TButton"
        )
        
        self._update_range_view()
    
    def _update_range_view(self):
        """Päivittää näytettävän aluenäkymän tilan mukaan"""
        if self.range_mode.get() == "fixed":
            self.custom_ranges_frame.pack_forget()
            self.fixed_ranges_frame.pack(fill=tk.X, pady=10)
        else:
            self.fixed_ranges_frame.pack_forget()
            self.custom_ranges_frame.pack(fill=tk.X, pady=10)
    
    def _on_file_selected(self, file_path):
        """Käsittelee tiedoston valinnan

        Args:
            file_path: Valitun tiedoston polku
        """
        try:
            self.current_file_path = file_path
            pdf_info = self.pdf_service.get_pdf_info(file_path)
            self.page_count = pdf_info["page_count"]
            
            file_name = os.path.basename(file_path)
            self.file_name_label.config(text=f"Tiedosto: {file_name}")
            self.page_info_label.config(text=f"Sivuja: {self.page_count}")
            
            if not self.custom_ranges:
                self._add_custom_range(1, self.page_count)
            self._create_custom_ranges_view()
            
            self._update_fixed_info()
            
            self.split_button.config(state=tk.NORMAL)
            
            self.status_label.config(text="")
        except Exception as e:
            self.status_label.config(text=f"Virhe: {str(e)}")
    
    def _update_fixed_info(self):
        """Päivittää kiinteiden alueiden tiedot"""
        if self.page_count > 0:
            try:
                pages_per_file = int(self.fixed_pages_count.get())
                if pages_per_file < 1:
                    pages_per_file = 1
                    self.fixed_pages_count.set("1")
                
                file_count = (self.page_count + pages_per_file - 1) // pages_per_file
                
                self.fixed_info_label.config(
                    text=f"Tämä PDF jaetaan tiedostoihin, joissa on {pages_per_file} sivua.\n"
                         f"{file_count} PDF-tiedostoa luodaan."
                )
            except ValueError:
                self.fixed_pages_count.set("2")
                self._update_fixed_info()
        else:
            self.fixed_info_label.config(text="Ei tiedostoa valittu.")
    
    def _split_pdf(self):
        """Jakaa PDF-tiedoston valittujen asetusten mukaan"""
        if not self.current_file_path:
            return
        
        try:
            output_dir = filedialog.askdirectory(title="Valitse tallennushakemisto")
            if not output_dir:
                return
            
            base_filename = os.path.splitext(os.path.basename(self.current_file_path))[0]
            
            if self.range_mode.get() == "fixed":
                pages_per_file = int(self.fixed_pages_count.get())
                output_files = self.pdf_service.split_by_fixed_range(
                    self.current_file_path, 
                    pages_per_file,
                    output_dir,
                    base_filename
                )
                self.status_label.config(
                    text=f"PDF jaettu onnistuneesti {len(output_files)} tiedostoon."
                )
            else:
                output_files = self.pdf_service.split_by_custom_ranges(
                    self.current_file_path,
                    self.custom_ranges,
                    output_dir,
                    base_filename
                )
                self.status_label.config(
                    text=f"PDF jaettu onnistuneesti {len(output_files)} tiedostoon."
                )
        except Exception as e:
            self.status_label.config(text=f"Virhe: {str(e)}")


def main():
    root = tk.Tk()
    app = PdfSplitterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()