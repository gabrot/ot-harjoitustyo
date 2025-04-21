"""
Säiliökomponenttien tyylimäärittelyt Scanflow-sovellukselle.

Tämä moduuli sisältää tyylimäärittelyt kaikille säiliötyyppisille komponenteille
kuten pudotusalueet, ryhmälaatikot ja muut säiliötyyppiset komponentit.
"""

from ui.styles.base_styles import BaseStyles

class ContainerStyles:
    """
    Säiliökomponenttien tyylimäärittelyjen luokka.
    
    Tarjoaa metodit erilaisten säiliökomponenttien, kuten ryhmälaatikoiden ja
    pudotusalueiden tyylien hallintaan ja soveltamiseen.
    """
    
    @classmethod
    def get_group_box_style(cls):
        """
        Palauttaa ryhmälaatikon tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely ryhmälaatikolle
        """
        return f"""
            QGroupBox {{
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
                border: 1px solid {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                margin-top: 20px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {BaseStyles.TEXT_PRIMARY};
            }}
        """
    
    @classmethod
    def get_group_box_content_style(cls):
        """
        Palauttaa ryhmälaatikon sisällön tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely ryhmälaatikon sisällölle
        """
        return f"""
            background-color: {BaseStyles.CARD_BG};
            min-height: 150px;
        """
    
    @classmethod
    def get_file_info_section_style(cls):
        """
        Palauttaa tiedostotietojen osion tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely tiedostotietojen osiolle
        """
        return f"""
            QFrame {{ 
                background-color: transparent; 
                border: none; 
                padding: 0px; 
                margin: 0px; 
            }}
        """
    
    @classmethod
    def get_drop_area_normal_style(cls):
        """
        Palauttaa pudotusalueen normaalin tilan tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely pudotusalueen normaalille tilalle
        """
        return f"""
            DropAreaWidget {{
                background-color: {BaseStyles.CARD_BG};
                border: 3px dashed {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_LARGE};
                padding: {BaseStyles.PADDING_LARGE};
                margin: 10px;
            }}
            DropAreaWidget:hover {{
                border-color: {BaseStyles.PRIMARY};
                background-color: #fffafa;
            }}
            QLabel {{
                background-color: transparent !important;
            }}
            QWidget {{
                background-color: transparent;
            }}
        """
    
    @classmethod
    def get_drop_area_drag_over_style(cls):
        """
        Palauttaa pudotusalueen raahauksen aikaisen tilan tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely pudotusalueen raahauksen aikaiselle tilalle
        """
        return f"""
            DropAreaWidget {{
                background-color: #f0f8ff;
                border: 3px dashed {BaseStyles.PRIMARY};
                border-radius: {BaseStyles.BORDER_RADIUS_LARGE};
                padding: {BaseStyles.PADDING_LARGE};
                margin: 10px;
            }}
            QLabel, QWidget {{
                background-color: transparent !important;
            }}
        """
    
    @classmethod
    def get_drop_label_style(cls):
        """
        Palauttaa pudotusalueen tekstin tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely pudotusalueen tekstille
        """
        return f"""
            font-size: {BaseStyles.FONT_SIZE_XLARGE}; 
            font-weight: {BaseStyles.FONT_WEIGHT_BOLD}; 
            color: {BaseStyles.TEXT_PRIMARY}; 
            margin-bottom: 10px; 
            border: none; 
            background: transparent;
        """
    
    @classmethod
    def get_or_label_style(cls):
        """
        Palauttaa pudotusalueen "tai"-tekstin tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely pudotusalueen "tai"-tekstille
        """
        return f"""
            font-size: {BaseStyles.FONT_SIZE_NORMAL}; 
            color: {BaseStyles.TEXT_SECONDARY}; 
            margin: 10px 0; 
            border: none; 
            background: transparent;
        """
    
    @classmethod
    def get_shrunk_drop_label_style(cls):
        """
        Palauttaa kutistetun pudotusalueen tekstin tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely kutistetun pudotusalueen tekstille
        """
        return f"""
            font-size: {BaseStyles.FONT_SIZE_MEDIUM};
            font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
            color: {BaseStyles.TEXT_PRIMARY};
            background-color: transparent !important;
        """
    
    @classmethod
    def get_shrunk_or_label_style(cls):
        """
        Palauttaa kutistetun pudotusalueen "tai"-tekstin tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely kutistetun pudotusalueen "tai"-tekstille
        """
        return f"""
            font-size: {BaseStyles.FONT_SIZE_NORMAL};
            color: {BaseStyles.TEXT_SECONDARY};
            margin: 0 12px;
            border: none;
            background: transparent;
        """
    
    @classmethod
    def get_explanation_text_style(cls):
        """
        Palauttaa selitystekstin tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely selitystekstille
        """
        return f"""
            color: {BaseStyles.TEXT_SECONDARY}; 
            font-size: {BaseStyles.FONT_SIZE_SMALL}; 
            margin-top: 5px;
        """
    
    @classmethod
    def get_separator_style(cls):
        """
        Palauttaa erottimen tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely erottimelle
        """
        return f"""
            background-color: {BaseStyles.BORDER_LIGHT}; 
            border: none; 
            max-height: 1px;
        """
    
    @classmethod
    def get_info_text_style(cls):
        """
        Palauttaa informaatiotekstin tyylimäärittelyn.
        
        Returns:
            str: CSS-tyylimäärittely informaatiotekstille
        """
        return f"""
            color: {BaseStyles.TEXT_SECONDARY}; 
            font-size: {BaseStyles.FONT_SIZE_SMALL};
        """
    
    @classmethod
    def apply_group_box_style(cls, group_box):
        """
        Soveltaa ryhmälaatikon tyylin annettuun komponenttiin.
        
        Args:
            group_box: QGroupBox-komponentti, johon tyyli sovelletaan
        """
        try:
            group_box.setStyleSheet(cls.get_group_box_style())
        except Exception as e:
            print(f"Virhe ryhmälaatikon tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_group_box_content_style(cls, content_widget):
        """
        Soveltaa ryhmälaatikon sisällön tyylin annettuun komponenttiin.
        
        Args:
            content_widget: QWidget-komponentti, johon tyyli sovelletaan
        """
        try:
            content_widget.setStyleSheet(cls.get_group_box_content_style())
        except Exception as e:
            print(f"Virhe ryhmälaatikon sisällön tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_file_info_section_style(cls, section):
        """
        Soveltaa tiedostotietojen osion tyylin annettuun komponenttiin.
        
        Args:
            section: QFrame-komponentti, johon tyyli sovelletaan
        """
        try:
            section.setStyleSheet(cls.get_file_info_section_style())
        except Exception as e:
            print(f"Virhe tiedostotietojen osion tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_drop_area_normal_style(cls, drop_area):
        """
        Soveltaa pudotusalueen normaalin tilan tyylin annettuun komponenttiin.
        
        Args:
            drop_area: DropAreaWidget-komponentti, johon tyyli sovelletaan
        """
        try:
            drop_area.setStyleSheet(cls.get_drop_area_normal_style())
        except Exception as e:
            print(f"Virhe pudotusalueen tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_drop_area_drag_over_style(cls, drop_area):
        """
        Soveltaa pudotusalueen raahauksen aikaisen tilan tyylin annettuun komponenttiin.
        
        Args:
            drop_area: DropAreaWidget-komponentti, johon tyyli sovelletaan
        """
        try:
            drop_area.setStyleSheet(cls.get_drop_area_drag_over_style())
        except Exception as e:
            print(f"Virhe pudotusalueen raahaustyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_drop_label_style(cls, label):
        """
        Soveltaa pudotusalueen tekstin tyylin annettuun komponenttiin.
        
        Args:
            label: QLabel-komponentti, johon tyyli sovelletaan
        """
        try:
            label.setStyleSheet(cls.get_drop_label_style())
        except Exception as e:
            print(f"Virhe pudotusalueen tekstin tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_or_label_style(cls, label):
        """
        Soveltaa pudotusalueen "tai"-tekstin tyylin annettuun komponenttiin.
        
        Args:
            label: QLabel-komponentti, johon tyyli sovelletaan
        """
        try:
            label.setStyleSheet(cls.get_or_label_style())
        except Exception as e:
            print(f"Virhe pudotusalueen 'tai'-tekstin tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_shrunk_drop_label_style(cls, label):
        """
        Soveltaa kutistetun pudotusalueen tekstin tyylin annettuun komponenttiin.
        
        Args:
            label: QLabel-komponentti, johon tyyli sovelletaan
        """
        try:
            label.setStyleSheet(cls.get_shrunk_drop_label_style())
        except Exception as e:
            print(f"Virhe kutistetun pudotusalueen tekstin tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_shrunk_or_label_style(cls, label):
        """
        Soveltaa kutistetun pudotusalueen "tai"-tekstin tyylin annettuun komponenttiin.
        
        Args:
            label: QLabel-komponentti, johon tyyli sovelletaan
        """
        try:
            label.setStyleSheet(cls.get_shrunk_or_label_style())
        except Exception as e:
            print(f"Virhe kutistetun pudotusalueen 'tai'-tekstin tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_explanation_text_style(cls, label):
        """
        Soveltaa selitystekstin tyylin annettuun komponenttiin.
        
        Args:
            label: QLabel-komponentti, johon tyyli sovelletaan
        """
        try:
            label.setStyleSheet(cls.get_explanation_text_style())
        except Exception as e:
            print(f"Virhe selitystekstin tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_separator_style(cls, frame):
        """
        Soveltaa erottimen tyylin annettuun komponenttiin.
        
        Args:
            frame: QFrame-komponentti, johon tyyli sovelletaan
        """
        try:
            frame.setStyleSheet(cls.get_separator_style())
        except Exception as e:
            print(f"Virhe erottimen tyylin soveltamisessa: {e}")
    
    @classmethod
    def apply_info_text_style(cls, label):
        """
        Soveltaa informaatiotekstin tyylin annettuun komponenttiin.
        
        Args:
            label: QLabel-komponentti, johon tyyli sovelletaan
        """
        try:
            label.setStyleSheet(cls.get_info_text_style())
        except Exception as e:
            print(f"Virhe informaatiotekstin tyylin soveltamisessa: {e}")