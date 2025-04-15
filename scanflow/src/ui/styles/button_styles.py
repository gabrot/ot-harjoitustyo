"""Sovelluksen painikkeiden tyylit.

Tämä moduuli sisältää tyylimäärittelyt erilaisille painikkeille (QPushButton),
joita käytetään sovelluksessa, kuten PDF-jakopainike ja alueiden
lisäyspainike. Jokainen vakio sisältää täydellisen Qt-tyylisäännöstön
tietylle painikkeen ulkoasulle ja käyttäytymiselle.
"""

SPLIT_BUTTON_STYLE = """
    QPushButton {
        font-size: 16px;
        min-height: 45px;
        background-color: #ec5f5f;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 8px 16px;
    }
    QPushButton:hover {
        background-color: #d45555;
    }
    QPushButton:pressed {
        background-color: #c04545;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #999999;
    }
"""

ADD_RANGE_BUTTON_STYLE = """
QPushButton {
    background-color: transparent;
    color: #ec5f5f;
    border: none;
    padding: 5px 10px;
    text-align: left;
    font-weight: 500;
}
QPushButton:hover {
    color: #d45555;
}
QPushButton:pressed {
    color: #c04545;
}
"""
