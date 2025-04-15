"""Pudotusalueen komponenttien tyylit.

Tämä moduuli sisältää tyylimäärittelyt tiedostojen pudotusalueelle
(DropAreaWidget) sekä sen eri tiloille (normaali, raahaus päällä) ja
sen sisällä oleville tekstielementeille ja painikkeille. Tyylit määrittelevät
ulkoasun sekä normaalissa että kutistetussa tilassa.
"""

DROP_AREA_NORMAL_STYLE = """
    DropAreaWidget {
        background-color: white;
        border: 3px dashed #ccc;
        border-radius: 8px;
        padding: 20px;
        margin: 10px;
    }
    DropAreaWidget:hover {
        border-color: #ec5f5f;
        background-color: #fffafa;
    }
    QLabel, QPushButton {
         background: transparent;
         border: none;
    }
    QPushButton {
        background-color: #ec5f5f;
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #d45555;
    }
"""

DROP_AREA_DRAG_OVER_STYLE = """
    DropAreaWidget {
        background-color: #f0f8ff;
        border: 3px dashed #ec5f5f;
        border-radius: 8px;
        padding: 20px;
        margin: 10px;
    }
    QLabel, QPushButton {
         background: transparent;
         border: none;
    }
"""

DROP_LABEL_STYLE = "font-size: 18px; font-weight: bold; color: #444; margin-bottom: 10px; border: none; background: transparent;"
OR_LABEL_STYLE = "font-size: 14px; color: #777; margin: 10px 0; border: none; background: transparent;"

SHRUNK_DROP_LABEL_STYLE = "font-size: 15px; font-weight: bold; color: #444; border: none; background: transparent;"
SHRUNK_OR_LABEL_STYLE = "font-size: 14px; color: #777; margin: 0 12px; border: none; background: transparent;"
