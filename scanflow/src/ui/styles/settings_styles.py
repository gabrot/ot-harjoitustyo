"""Asetuskomponenttien tyylit ScanFlow-sovelluksessa.

Tämä moduuli sisältää Qt-tyylisäännöstöt (CSS-tyylisiä merkkijonoja)
erilaisille käyttöliittymäkomponenteille, joita käytetään PDF-jakamisen
asetusten määrittelyyn, kuten ryhmälaatikot, syöttökentät ja painikkeet
sekä kiinteän että mukautetun jakamisen asetuksissa.
"""

RANGE_INPUT_STYLE = """
    QSpinBox {
        padding: 3px;
        border: 1px solid #ddd;
        border-radius: 3px;
        min-width: 60px;
        background-color: white;
        color: black;
    }
"""

REMOVE_RANGE_BUTTON_STYLE = """
    QPushButton {
        background-color: #e74c3c;
        color: white;
        border: none;
        padding: 2px 6px;
        border-radius: 3px;
        min-width: 24px; 
        max-width: 24px;
        min-height: 24px;
        max-height: 24px;
        font-weight: bold; 
    }
    QPushButton:hover {
        background-color: #c0392b;
    }
"""
