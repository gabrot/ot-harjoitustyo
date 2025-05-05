"""
Moduuli PDF-tiedoston kiinteän sivumäärän jakokomponentille.

Tarjoaa `FixedRangeSettings`-komponentin, jolla käyttäjä voi määrittää
kuinka monta sivua kuhunkin jaettuun PDF-tiedostoon tulee, kun käytetään
kiinteää jakotapaa.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSlot
from src.ui.styles.dialog_styles import DialogStyles
from src.ui.styles.container_styles import ContainerStyles


class FixedRangeSettings(QWidget):
    """
    Komponentti PDF-tiedoston kiinteän sivumäärän jakamisasetuksille.

    Tarjoaa käyttöliittymän, jossa käyttäjä voi määrittää kuinka monta
    sivua kuhunkin osatiedostoon tulee, kun PDF jaetaan tasaisesti.
    Näyttää myös tiedon siitä, kuinka moneen osaan tiedosto jaetaan ja
    miten sivut jakautuvat.
    """

    def __init__(self, parent=None):
        """
        Alustaa kiinteän jaon asetuskomponentin.

        Args:
            parent (QWidget, optional): Isäntäwidget. Oletus None.
        """
        super().__init__(parent)
        self._page_count = 0
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)

        pages_label = QLabel("Sivuja per tiedosto:")
        input_layout.addWidget(pages_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.pages_spinner = QSpinBox()
        self.pages_spinner.setMinimum(1)
        self.pages_spinner.setMaximum(1000)
        self.pages_spinner.setValue(1)
        DialogStyles.apply_range_input_style(self.pages_spinner)
        self.pages_spinner.valueChanged.connect(self._update_info_text)
        input_layout.addWidget(self.pages_spinner)
        input_layout.addStretch(1)

        layout.addLayout(input_layout)

        explanation = QLabel(
            "Määritä kuinka monta sivua kuhunkin jaettuun PDF-tiedostoon tulee. "
            "Viimeinen tiedosto voi sisältää vähemmän sivuja."
        )
        explanation.setWordWrap(True)
        ContainerStyles.apply_explanation_text_style(explanation)
        layout.addWidget(explanation)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        ContainerStyles.apply_separator_style(separator)
        layout.addWidget(separator)

        self.file_count_info = QLabel("")
        ContainerStyles.apply_info_text_style(self.file_count_info)
        layout.addWidget(self.file_count_info)

        self.page_distribution_info = QLabel("")
        ContainerStyles.apply_info_text_style(self.page_distribution_info)
        layout.addWidget(self.page_distribution_info)

        layout.addStretch(1)

    @pyqtSlot(int)
    def _update_info_text(self, _=None):
        pages_per_file = self.pages_spinner.value()

        if self._page_count <= 0:
            self.file_count_info.setText("Ei sivuja valitussa tiedostossa.")
            self.page_distribution_info.setText("")
            return

        if pages_per_file <= 0:
             self.file_count_info.setText("Sivuja per tiedosto ei voi olla nolla.")
             self.page_distribution_info.setText("")
             return

        full_files = self._page_count // pages_per_file
        remaining_pages = self._page_count % pages_per_file
        total_files = full_files + (1 if remaining_pages > 0 else 0)

        self.file_count_info.setText(f"Tiedosto jaetaan {total_files} osaan.")

        if remaining_pages == 0:
            if total_files == 1:
                 self.page_distribution_info.setText(
                    f"Ainoa osa sisältää {pages_per_file} sivua."
                )
            else:
                self.page_distribution_info.setText(
                    f"Jokainen osa sisältää {pages_per_file} sivua."
                )
        else:
            if full_files == 0:
                 self.page_distribution_info.setText(
                    f"Ainoa osa sisältää {remaining_pages} sivua."
                )
            else:
                self.page_distribution_info.setText(
                    f"{full_files} osaa sisältää {pages_per_file} sivua, "
                    f"viimeinen osa sisältää {remaining_pages} sivua."
                )

    def update_page_count(self, page_count):
        """
        Päivittää komponentin tiedon PDF-tiedoston kokonaissivumäärästä.

        Asettaa myös sivumäärän valintakomponentin (QSpinBox) maksimiarvoksi
        annetun sivumäärän (tai 1, jos sivumäärä on 0 tai negatiivinen) ja
        päivittää informaatiotekstit.

        Args:
            page_count (int): PDF-tiedoston kokonaissivumäärä.
        """
        self._page_count = max(0, page_count)
        max_pages = max(1, self._page_count)
        self.pages_spinner.setMaximum(max_pages)
        self.pages_spinner.setValue(min(self.pages_spinner.value(), max_pages))
        self._update_info_text()

    def get_pages_per_file(self):
        """
        Palauttaa käyttäjän valitseman sivumäärän per jaettava tiedosto.

        Returns:
            int: Käyttäjän QSpinBox-komponenttiin asettama arvo.
        """
        return self.pages_spinner.value()
