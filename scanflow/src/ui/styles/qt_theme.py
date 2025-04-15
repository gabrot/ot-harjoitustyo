"""QtTheme-luokka ja globaalit tyylit ScanFlow-sovellukselle.

Määrittelee sovelluksen väripaletin ja yleiset tyylisäännöt
PyQt-käyttöliittymäkomponenteille. Tarjoaa `get_stylesheet`-metodin
sovelluksen tyylisäännöstön hakemiseen.
"""


class QtTheme:
    """PyQt-yhteensopiva teemaluokka ScanFlow-sovellukselle.

    Määrittelee sovelluksen väripaletin ja tarjoaa pääsyn siihen.

    Attributes:
        PRIMARY (str): Sovelluksen pääväri (esim. painikkeet, korostukset).
        PRIMARY_HOVER (str): Päävärin hover-tila.
        SUCCESS (str): Onnistumisen ilmaisuväri (esim. ilmoitukset).
        ERROR (str): Virheen ilmaisuväri (esim. ilmoitukset, validoinnit).
        BACKGROUND (str): Sovelluksen päätaustaväri.
        CARD_BG (str): Korttimaisten elementtien (esim. QGroupBox) taustaväri.
        BORDER (str): Yleinen reunaviivan väri.
        BORDER_LIGHT (str): Kevyempi reunaviivan väri.
        TEXT_PRIMARY (str): Ensisijainen tekstiväri.
        TEXT_SECONDARY (str): Toissijainen (harmaampi) tekstiväri.
        TEXT_DARK (str): Tumma tekstiväri.
    """

    PRIMARY = "#ec5f5f"
    PRIMARY_HOVER = "#d64c4c"
    SUCCESS = "#28a745"
    ERROR = "#dc3545"
    BACKGROUND = "#f8f9fa"
    CARD_BG = "#ffffff"
    BORDER = "#dee2e6"
    BORDER_LIGHT = "#e9ecef"
    TEXT_PRIMARY = "#495057"
    TEXT_SECONDARY = "#6c757d"
    TEXT_DARK = "#343a40"

    @classmethod
    def get_stylesheet(cls):
        """Palauttaa sovelluksen globaalin tyylisäännöstön.

        Muotoilee CSS-tyylisen merkkijonon PyQt:n käyttämään muotoon
        käyttäen luokassa määriteltyjä värejä ja attribuutteja.

        Returns:
            str: Koko sovelluksen tyylisäännöstö merkkijonona.
        """
        return f"""
            QMainWindow {{
                background-color: {cls.BACKGROUND};
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {cls.BORDER};
                border-radius: 6px;
                margin-top: 1ex;
                padding: 15px;
                background-color: {cls.CARD_BG};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                background-color: {cls.BACKGROUND};
                color: {cls.TEXT_PRIMARY};
                font-size: 15px;
            }}
            QLabel {{
                font-size: 14px;
                color: {cls.TEXT_PRIMARY};
            }}
            QPushButton {{
                background-color: {cls.PRIMARY};
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {cls.PRIMARY_HOVER};
            }}
            QPushButton:disabled {{
                background-color: {cls.BORDER};
                color: {cls.TEXT_SECONDARY};
            }}
            QSpinBox {{
                padding: 6px;
                border: 1px solid {cls.BORDER};
                border-radius: 3px;
                font-size: 14px;
                color: {cls.TEXT_PRIMARY};
                background-color: {cls.CARD_BG};
            }}
            QRadioButton {{
                font-size: 14px;
                color: {cls.TEXT_PRIMARY};
                padding: 5px 0;
            }}

            QFrame#RangeFrame {{
                border: 1px solid {cls.BORDER};
                border-radius: 4px;
                background-color: {cls.BACKGROUND};
                margin-bottom: 8px;
            }}
            QPushButton#DeleteRangeButton {{
                background-color: {cls.BACKGROUND};
                color: {cls.ERROR};
                border: 1px solid {cls.BORDER};
                border-radius: 12px;
                font-weight: bold;
                font-size: 12px;
                padding: 0px;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
            }}
            QPushButton#DeleteRangeButton:hover {{
                background-color: {cls.ERROR};
                color: white;
                border: 1px solid {cls.ERROR};
            }}
            QPushButton#AddRangeButton {{
                background-color: {cls.CARD_BG};
                color: {cls.SUCCESS};
                border: 1px solid {cls.SUCCESS};
                font-weight: bold;
                padding: 8px 16px;
                margin-top: 10px;
            }}
            QPushButton#AddRangeButton:hover {{
                background-color: {cls.SUCCESS};
                color: white;
            }}
            #StatusLabel {{
                color: {cls.TEXT_PRIMARY};
                font-size: 13px;
                padding: 5px;
            }}
            #ErrorLabel {{
                color: {cls.ERROR};
                font-weight: bold;
            }}
            #SuccessLabel {{
                color: {cls.SUCCESS};
                font-weight: bold;
            }}
            #FileNameLabel {{
                font-weight: bold;
                font-size: 15px;
                color: {cls.TEXT_PRIMARY};
            }}
            #PageCountLabel {{
                font-size: 14px;
                color: {cls.TEXT_SECONDARY};
            }}
            QWidget {{
            }}
            QFrame#NotificationOverlay {{
                z-index: 1000;
                max-width: 80%;
            }}
        """
