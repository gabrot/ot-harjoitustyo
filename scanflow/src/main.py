"""Sovelluksen päämoduuli ja käynnistyspiste.

Tämä moduuli alustaa ja käynnistää ScanFlow-sovelluksen graafisen
käyttöliittymän käyttäen PyQt6-kirjastoa.
"""

import sys
from PyQt6 import QtWidgets
from src.ui.app import MainWindow


def main():
    """Sovelluksen pääfunktio.

    Luo QApplication-instanssin ja MainWindow-pääikkunan, näyttää ikkunan
    ja käynnistää sovelluksen tapahtumasilmukan.
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
