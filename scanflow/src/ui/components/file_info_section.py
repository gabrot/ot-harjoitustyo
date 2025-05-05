"""
Moduuli ladatun PDF-tiedoston tietojen näyttämiseksi.

Tarjoaa `FileInfoSection`-komponentin, joka näyttää ladatun PDF:n
nimen ja sivumäärän sekä painikkeen tiedoston poistamiseksi näkymästä.
"""

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from src.ui.styles.container_styles import ContainerStyles
from src.ui.styles.button_styles import ButtonStyles


class FileInfoSection(QFrame):
    """
    Komponentti ladatun PDF-tiedoston perustietojen näyttämiseen.

    Näyttää tiedoston nimen ja sivumäärän. Sisältää myös painikkeen,
    jolla käyttäjä voi "poistaa" tiedoston sovelluksen näkymästä, mikä
    palauttaa käyttöliittymän tilaan, jossa uusi tiedosto voidaan ladata.

    Signals:
        file_removed: Lähetetään, kun poistopainiketta painetaan.
                      Ei sisällä argumentteja.
    """

    file_removed = pyqtSignal()

    def __init__(self, parent=None):
        """
        Alustaa tiedostotieto-osion.

        Args:
            parent (QWidget, optional): Isäntäwidget. Oletus None.
        """
        super().__init__(parent)
        ContainerStyles.apply_file_info_section_style(self)
        self._init_ui()
        self.setVisible(False)

    def _init_ui(self):
        """Alustaa osion sisäiset käyttöliittymäkomponentit."""
        file_info_layout = QHBoxLayout(self)
        file_info_layout.setContentsMargins(5, 5, 5, 5)
        file_info_layout.setSpacing(10)

        file_info_text_widget = QWidget()
        text_layout = QVBoxLayout(file_info_text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)

        self.file_name_label = QLabel("Ei tiedostoa valittuna")
        self.file_name_label.setObjectName("FileNameLabel")
        self.file_name_label.setWordWrap(True)
        text_layout.addWidget(self.file_name_label)

        self.page_count_label = QLabel("")
        self.page_count_label.setObjectName("PageCountLabel")
        text_layout.addWidget(self.page_count_label)

        file_info_layout.addWidget(file_info_text_widget, stretch=1)

        remove_file_btn = QPushButton("×")
        ButtonStyles.apply_delete_button_style(remove_file_btn)
        remove_file_btn.setToolTip("Poista tiedosto näkymästä")
        remove_file_btn.setFixedSize(28, 28)
        remove_file_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_file_btn.clicked.connect(self._on_remove_clicked)
        file_info_layout.addWidget(
            remove_file_btn,
            alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        )
        self.remove_file_btn = remove_file_btn

    def _on_remove_clicked(self):
        self.file_removed.emit()

    def update_file_info(self, file_name, page_count):
        """
        Päivittää näytettävät tiedostotiedot ja näyttää osion.

        Args:
            file_name (str): Näytettävän tiedoston nimi.
            page_count (int): Näytettävän tiedoston sivumäärä.
        """
        self.file_name_label.setText(f"{file_name}")
        self.page_count_label.setText(f"Sivuja: {page_count}")
        self.setVisible(True)

    def clear(self):
        self.file_name_label.setText("Ei tiedostoa valittuna")
        self.page_count_label.setText("")
        self.setVisible(False)

    def get_current_filename(self):
        """
        Palauttaa tällä hetkellä näytettävän tiedoston nimen.

        Returns:
            str: Tiedoston nimi, tai tyhjä merkkijono jos ei tiedostoa.
        """
        return self.file_name_label.text() if self.isVisible() else ""
