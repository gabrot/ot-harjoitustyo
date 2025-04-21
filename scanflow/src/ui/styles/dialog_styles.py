"""
Dialogien ja ilmoitusten tyylimäärittelyt Scanflow-sovellukselle.

Tämä moduuli sisältää tyylimäärittelyt dialogeille, ilmoituksille ja
erilaisille asetuskomponenteille. Tyylimäärittelyt on toteutettu
CSS-tyylisäännöstöillä, jotka voidaan soveltaa sopiviin komponentteihin.
"""

from ui.styles.base_styles import BaseStyles
from ui.styles.button_styles import ButtonStyles


class DialogStyles:
    """
    Dialogien ja ilmoitusten tyylimäärittelyjen luokka.
    
    Tarjoaa metodit erilaisten dialogien, ilmoitusten ja asetuskomponenttien 
    tyylien hallintaan ja soveltamiseen.
    """
    
    @classmethod
    def get_notification_frame_style(cls, bg_color, border_color):
        """
        Palauttaa ilmoituskehyksen tyylin.
        
        Args:
            bg_color: Taustaväri
            border_color: Reunaväri
            
        Returns:
            str: CSS-tyylimäärittely
        """
        return f"""
            QFrame#NotificationOverlay {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
            }}
        """
    
    @classmethod
    def get_notification_label_style(cls, text_color):
        """
        Palauttaa ilmoitustekstin tyylin.
        
        Args:
            text_color: Tekstin väri
            
        Returns:
            str: CSS-tyylimäärittely
        """
        return f"""
            color: {text_color}; 
            font-size: {BaseStyles.FONT_SIZE_NORMAL}; 
            font-weight: {BaseStyles.FONT_WEIGHT_MEDIUM}; 
            background: transparent; 
            border: none;
        """
    
    @classmethod
    def get_close_button_style(cls, close_color):
        """
        Palauttaa ilmoituksen sulkunapin tyylin.
        
        Args:
            close_color: Sulkunapin väri
            
        Returns:
            str: CSS-tyylimäärittely
        """
        return f"""
            QPushButton {{ 
                background: transparent; 
                border: none; 
                color: {close_color}; 
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD}; 
                font-size: 20px; 
                padding: 0 0 2px 0; 
            }}
            QPushButton:hover {{ 
                color: #000; 
            }}
        """
    
    @classmethod
    def get_range_input_style(cls):
        """
        Palauttaa sivualuekenttien tyylin.
        
        Returns:
            str: CSS-tyylimäärittely
        """
        return f"""
            QSpinBox {{
                padding: 3px;
                border: 1px solid {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_SMALL};
                min-width: 60px;
                background-color: {BaseStyles.CARD_BG};
                color: {BaseStyles.TEXT_PRIMARY};
            }}
        """
    
    @classmethod
    def get_scrollarea_style(cls):
        """
        Palauttaa vieritysalueen tyylin.
        
        Returns:
            str: CSS-tyylimäärittely
        """
        return f"""
            QScrollArea {{ 
                background-color: transparent; 
                border: none; 
            }}
            QScrollBar:vertical {{ 
                background-color: transparent; 
                width: 8px; 
                margin: 0; 
                border-radius: 4px; 
            }}
            QScrollBar::handle:vertical {{ 
                background-color: #cccccc; 
                border-radius: 4px; 
                min-height: 25px; 
            }}
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {{ 
                height: 0px; 
                background: none; 
            }}
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {{ 
                background: none; 
            }}
        """
    
    @classmethod
    def apply_notification_style(cls, container, label, close_button, notification_type="info"):
        """
        Soveltaa ilmoituksen tyylit annettuihin komponentteihin.
        
        Args:
            container: QFrame-komponentti, johon ilmoituskehyksen tyyli sovelletaan
            label: QLabel-komponentti, johon tekstin tyyli sovelletaan
            close_button: QPushButton-komponentti sulkunapiksi
            notification_type: Ilmoituksen tyyppi ('error', 'success', 'info')
        """
        bg_color, text_color, border_color, close_color = BaseStyles.get_notification_colors(notification_type)
        
        try:
            container.setStyleSheet(cls.get_notification_frame_style(bg_color, border_color))
            label.setStyleSheet(cls.get_notification_label_style(text_color))
            close_button.setStyleSheet(cls.get_close_button_style(close_color))
        except Exception as e:
            print(f"Virhe ilmoituksen tyylien soveltamisessa: {e}")
    
    @classmethod
    def apply_range_input_style(cls, spinbox):
        """
        Soveltaa sivualuekentän tyylin annettuun komponenttiin.
        
        Args:
            spinbox: QSpinBox-komponentti, johon tyyli sovelletaan
        """
        try:
            spinbox.setStyleSheet(cls.get_range_input_style())
        except Exception as e:
            print(f"Virhe sivualuekentän tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_scrollarea_style(cls, scrollarea):
        """
        Soveltaa vieritysalueen tyylin annettuun komponenttiin.
        
        Args:
            scrollarea: QScrollArea-komponentti, johon tyyli sovelletaan
        """
        try:
            scrollarea.setStyleSheet(cls.get_scrollarea_style())
        except Exception as e:
            print(f"Virhe vieritysalueen tyylin soveltamisessa: {e}")