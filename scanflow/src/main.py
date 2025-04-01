import tkinter as tk
from tkinter import ttk

from ui.app import PdfSplitterApp
from ui.theme import setup_styles


def main():
    """Sovelluksen käynnistysfunktio"""
    root = tk.Tk()
    root.title("Scanflow PDF Splitter")
    
    style = ttk.Style()
    style.theme_use('default')
    setup_styles(style)
    
    app = PdfSplitterApp(root)
    
    root.mainloop()


if __name__ == "__main__":
    main()