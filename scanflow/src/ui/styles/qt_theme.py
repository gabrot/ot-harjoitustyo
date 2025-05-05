"""
QtTheme-luokka ja globaalit tyylit Scanflow-sovellukselle.

Määrittelee sovelluksen väripaletin ja yleiset tyylisäännöt
PyQt-käyttöliittymäkomponenteille. Tarjoaa `get_stylesheet`-metodin
sovelluksen tyylisäännöstön hakemiseen.
"""

from src.ui.styles.base_styles import BaseStyles

class QtTheme:
    """
    PyQt-yhteensopiva teemaluokka Scanflow-sovellukselle.

    Hyödyntää BaseStyles-luokan määrittelemää väripalettia ja tarjoaa
    koko sovelluksen tyylisäännöstön.
    """
    
    @classmethod
    def get_stylesheet(cls):
        """
        Palauttaa sovelluksen globaalin tyylisäännöstön.

        Returns:
            str: Koko sovelluksen tyylisäännöstö merkkijonona.
        """
        return f"""
            QMainWindow {{
                background-color: {BaseStyles.BACKGROUND};
            }}
            QGroupBox {{
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
                border: 1px solid {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_LARGE};
                margin-top: 1ex;
                padding: {BaseStyles.PADDING_MEDIUM};
                background-color: {BaseStyles.CARD_BG};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                background-color: {BaseStyles.BACKGROUND};
                color: {BaseStyles.TEXT_PRIMARY};
                font-size: {BaseStyles.FONT_SIZE_MEDIUM};
            }}
            QLabel {{
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
                color: {BaseStyles.TEXT_PRIMARY};
            }}
            QPushButton {{
                background-color: {BaseStyles.PRIMARY};
                color: {BaseStyles.TEXT_LIGHT};
                border: none;
                padding: 10px 18px;
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
            }}
            QPushButton:hover {{
                background-color: {BaseStyles.PRIMARY_HOVER};
            }}
            QPushButton:disabled {{
                background-color: {BaseStyles.DISABLED_BG};
                color: {BaseStyles.DISABLED_TEXT};
            }}
            QSpinBox {{
                padding: 6px;
                border: 1px solid {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_SMALL};
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
                color: {BaseStyles.TEXT_PRIMARY};
                background-color: {BaseStyles.CARD_BG};
            }}
            QLineEdit {{
                padding: 6px 10px;
                border: 1px solid {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
                color: {BaseStyles.TEXT_PRIMARY};
                background-color: {BaseStyles.CARD_BG};
            }}
            QRadioButton {{
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
                color: {BaseStyles.TEXT_PRIMARY};
                padding: 5px 0;
            }}

            QFrame#RangeFrame {{
                border: 1px solid {BaseStyles.BORDER};
                border-radius: {BaseStyles.BORDER_RADIUS_NORMAL};
                background-color: {BaseStyles.BACKGROUND};
                margin-bottom: 8px;
            }}

            QPushButton#DeleteRangeButton {{
                background-color: transparent;
                color: {BaseStyles.ERROR};
                border: 1px solid {BaseStyles.BORDER};
                border-radius: 14px;
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
                padding: 0px;
                min-width: 28px;
                max-width: 28px;
                min-height: 28px;
                max-height: 28px;
            }}
            QPushButton#DeleteRangeButton:hover {{
                background-color: {BaseStyles.PRIMARY};
                color: {BaseStyles.TEXT_LIGHT};
                border: 1px solid {BaseStyles.PRIMARY};
            }}

            QPushButton#AddRangeButton {{
                background-color: {BaseStyles.CARD_BG};
                color: {BaseStyles.SUCCESS};
                border: 1px solid {BaseStyles.SUCCESS};
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
                padding: 8px 16px;
                margin-top: 10px;
            }}
            QPushButton#AddRangeButton:hover {{
                background-color: {BaseStyles.SUCCESS};
                color: {BaseStyles.TEXT_LIGHT};
            }}
            #StatusLabel {{
                color: {BaseStyles.TEXT_PRIMARY};
                font-size: {BaseStyles.FONT_SIZE_SMALL};
                padding: 5px;
            }}
            #ErrorLabel {{
                color: {BaseStyles.ERROR};
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
            }}
            #SuccessLabel {{
                color: {BaseStyles.SUCCESS};
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
            }}
            #FileNameLabel {{
                font-weight: {BaseStyles.FONT_WEIGHT_BOLD};
                font-size: {BaseStyles.FONT_SIZE_MEDIUM};
                color: {BaseStyles.TEXT_PRIMARY};
            }}
            #PageCountLabel {{
                font-size: {BaseStyles.FONT_SIZE_NORMAL};
                color: {BaseStyles.TEXT_SECONDARY};
            }}
            QWidget {{
                background-color: {BaseStyles.BACKGROUND};
            }}
            QDialog, QMessageBox {{
                background-color: {BaseStyles.BACKGROUND};
            }}
            QFrame#NotificationOverlay {{
                max-width: 80%;
            }}
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QScrollBar:vertical {{
                width: 0px;
                background: transparent;
            }}
            QScrollBar:horizontal {{
                height: 0px;
                background: transparent;
            }}
            QScrollBar:vertical:hover,
            QScrollBar:horizontal:hover {{
                background: {BaseStyles.BACKGROUND};
            }}
            QScrollBar:vertical:hover {{
                width: 12px;
            }}
            QScrollBar:horizontal:hover {{
                height: 12px;
            }}
            QScrollBar::handle:vertical:hover,
            QScrollBar::handle:horizontal:hover {{
                background: {BaseStyles.PRIMARY};
                border-radius: 6px;
            }}
            QScrollBar::add-line,
            QScrollBar::sub-line {{
                width: 0px;
                height: 0px;
            }}
        """
