"""
Painikkeiden tyylit.
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

from src.ui.styles.base_styles import BaseStyles

class ButtonStyles:
    """
    Painikkeiden tyylimäärittelyjen luokka.
    
    Tarjoaa metodit erilaisten painikkeiden tyylien hallintaan ja soveltamiseen.
    """
    
    @classmethod
    def get_primary_button_style(cls):
        """
        Palauttaa ensisijaisen toimintapainikkeen tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely ensisijaiselle painikkeelle
        """
        return f"""
            QPushButton {{
                background-color: {BaseStyles.PRIMARY};
                color: {BaseStyles.TEXT_LIGHT};
                border: none;
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                padding: 16px 16px;
                font-weight: {BaseStyles.FONT_WEIGHT_MEDIUM};
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {BaseStyles.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {BaseStyles.PRIMARY_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {BaseStyles.DISABLED_BG};
                color: {BaseStyles.DISABLED_TEXT};
            }}
        """
    
    @classmethod
    def get_browse_button_style(cls):
        """
        Palauttaa tiedoston selaus -painikkeen tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely selauspainikkeelle
        """
        return f"""
            QPushButton#BrowseButton {{
                background-color: transparent;
                color: {BaseStyles.PRIMARY};
                border: 1px solid {BaseStyles.PRIMARY};
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                padding: 8px 10px;
                font-weight: {BaseStyles.FONT_WEIGHT_MEDIUM};
            }}
            QPushButton#BrowseButton:hover {{
                background-color: {BaseStyles.PRIMARY};
                color: {BaseStyles.TEXT_LIGHT};
            }}
        """
    
    @classmethod
    def get_browse_output_button_style(cls):
        """
        Palauttaa tallennuskansion selaus -painikkeen tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely selauspainikkeelle
        """
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                padding: 7px 10px;
                color: {BaseStyles.TEXT_PRIMARY};
                font-weight: {BaseStyles.FONT_WEIGHT_NORMAL};
            }}
            QPushButton:hover {{
                background-color: {BaseStyles.PRIMARY};
                color: {BaseStyles.TEXT_LIGHT};
            }}
        """
    
    @classmethod
    def get_delete_button_style(cls):
        """
        Palauttaa poistopainikkeen tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely poistopainikkeelle
        """
        return f"""
            QPushButton {{
                background-color: {BaseStyles.ERROR};
                color: {BaseStyles.TEXT_LIGHT};
                border: none;
                padding: 2px 6px;
                border-radius: {BaseStyles.BORDER_RADIUS_SMALL};
                min-width: 24px; 
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD}; 
            }}
            QPushButton:hover {{
                background-color: #c0392b;
            }}
        """
    
    @classmethod
    def get_add_range_button_style(cls):
        """
        Palauttaa sivualueiden lisäyspainikkeen tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely lisäyspainikkeelle
        """
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {BaseStyles.INFO};
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                padding: 5px 10px;
                color: {BaseStyles.INFO};
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
            }}
            QPushButton:hover {{
                background-color: {BaseStyles.INFO};
                color: {BaseStyles.TEXT_LIGHT};
            }}
            QPushButton:disabled {{
                border: 1px solid {BaseStyles.DISABLED_BG};
                color: {BaseStyles.DISABLED_TEXT};
            }}
        """
    
    @classmethod
    def apply_primary_style(cls, button):
        """
        Soveltaa ensisijaisen painikkeen tyylin annettuun komponenttiin.
        
        Args:
            button: QPushButton-komponentti, johon tyyli sovelletaan
        """
        try:
            button.setStyleSheet(cls.get_primary_button_style())
        except Exception as e:
            print(f"Virhe ensisijaisen painikkeen tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_browse_button_style(cls, button):
        """
        Soveltaa selauspainikkeen tyylin annettuun komponenttiin.
        
        Args:
            button: QPushButton-komponentti, johon tyyli sovelletaan
        """
        try:
            button.setObjectName("BrowseButton")
            button.setStyleSheet(cls.get_browse_button_style())
        except Exception as e:
            print(f"Virhe selauspainikkeen tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_browse_output_style(cls, button):
        """
        Soveltaa tallennuskansion selauspainikkeen tyylin annettuun komponenttiin.
        
        Args:
            button: QPushButton-komponentti, johon tyyli sovelletaan
        """
        try:
            button.setStyleSheet(cls.get_browse_output_button_style())
        except Exception as e:
            print(f"Virhe tallennuskansio-painikkeen tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_delete_button_style(cls, button):
        """
        Soveltaa poistopainikkeen tyylin annettuun komponenttiin.
        
        Args:
            button: QPushButton-komponentti, johon tyyli sovelletaan
        """
        try:
            button.setObjectName("DeleteRangeButton")
            button.setStyleSheet(cls.get_delete_button_style())
        except Exception as e:
            print(f"Virhe poistopainikkeen tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_add_range_style(cls, button):
        """
        Soveltaa alueen lisäyspainikkeen tyylin annettuun komponenttiin.
        
        Args:
            button: QPushButton-komponentti, johon tyyli sovelletaan
        """
        try:
            button.setObjectName("AddRangeButton")
            button.setStyleSheet(cls.get_add_range_button_style())
        except Exception as e:
            print(f"Virhe lisäyspainikkeen tyylin soveltamisessa: {e}")
