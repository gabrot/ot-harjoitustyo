"""Sovelluksen ryhmälaatikkojen (QGroupBox) tyylit.

Tämä moduuli määrittelee QGroupBox-komponenttien yhtenäisen ulkoasun
sovelluksessa. Ryhmälaatikoita käytetään käyttöliittymän eri osioiden,
kuten asetusten ja tiedostotietojen, visuaaliseen jäsentämiseen.
"""

COMMON_GROUP_BOX_STYLE = """
    QGroupBox {
        background-color: white;
        font-weight: bold;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-top: 20px;
        padding-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
        color: black;
    }
"""

GROUP_BOX_CONTENT_STYLE = """
    background-color: white;
    min-height: 150px;
"""
