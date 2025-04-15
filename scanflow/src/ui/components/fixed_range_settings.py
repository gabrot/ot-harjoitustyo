"""Moduuli kiinteän sivumäärän PDF-jakamisasetuksille."""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QGroupBox,
    QFrame,
)
from ui.styles.group_styles import COMMON_GROUP_BOX_STYLE

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


class FixedRangeSettings(QWidget):
    """Widget PDF:n jakamiseksi osiin, joissa on kiinteä määrä sivuja."""

    def __init__(self, parent: Optional[QWidget] = None):
        """Alustaa kiinteän sivumäärän jakamisasetukset."""
        super().__init__(parent)
        self.page_count = 0
        self._init_ui()

    def _init_ui(self):
        """Alustaa widgetin käyttöliittymäkomponentit."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.settings_group = QGroupBox("Sivumääräkohtaiset asetukset")
        self.settings_group.setStyleSheet(COMMON_GROUP_BOX_STYLE)
        group_layout = QVBoxLayout(self.settings_group)

        pages_layout = QHBoxLayout()
        pages_label = QLabel("Sivuja per tiedosto:")
        self.pages_spinner = QSpinBox()
        self.pages_spinner.setMinimum(1)
        self.pages_spinner.setMaximum(9999)
        self.pages_spinner.setValue(2)
        self.pages_spinner.setStyleSheet(RANGE_INPUT_STYLE)
        self.pages_spinner.setToolTip(
            "Kuinka monta sivua tulee yhteen uuteen PDF-tiedostoon."
        )
        self.pages_spinner.valueChanged.connect(self._update_info_labels)

        pages_layout.addWidget(pages_label)
        pages_layout.addWidget(self.pages_spinner)
        pages_layout.addStretch(1)
        group_layout.addLayout(pages_layout)

        explanation = QLabel(
            "Tiedosto jaetaan useisiin PDF-tiedostoihin, joissa jokaisessa "
            "on määritetty määrä sivuja (paitsi mahdollisesti viimeisessä)."
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet("color: #555; font-size: 13px; margin-top: 5px;")
        group_layout.addWidget(explanation)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(
            "background-color: #eee; margin-top: 15px; margin-bottom: 10px; height: 1px;"
        )
        group_layout.addWidget(separator)

        self.file_count_info = QLabel("")
        self.file_count_info.setWordWrap(True)
        self.file_count_info.setStyleSheet(
            "color: #333; font-weight: bold; font-size: 13px;"
        )
        group_layout.addWidget(self.file_count_info)

        self.page_distribution_info = QLabel("")
        self.page_distribution_info.setWordWrap(True)
        self.page_distribution_info.setStyleSheet("color: #555; font-size: 13px;")
        group_layout.addWidget(self.page_distribution_info)

        group_layout.addStretch(1)
        layout.addWidget(self.settings_group)
        self._update_info_labels()

    def _update_info_labels(self):
        """Päivittää informatiiviset labelit."""
        if self.page_count <= 0:
            self.file_count_info.setText("")
            self.page_distribution_info.setText("")
            self.pages_spinner.setEnabled(False)
            return

        self.pages_spinner.setEnabled(True)
        pages_per_file = self.pages_spinner.value()
        if pages_per_file <= 0:
            self.file_count_info.setText("Virheellinen sivumäärä.")
            self.page_distribution_info.setText("")
            return

        import math

        total_files = math.ceil(self.page_count / pages_per_file)
        full_files = self.page_count // pages_per_file
        remaining_pages = self.page_count % pages_per_file

        self.file_count_info.setText(f"Luodaan {total_files} uutta PDF-tiedostoa.")

        dist_text = ""
        if total_files == 1:
            dist_text = f"Tiedosto sisältää kaikki {self.page_count} sivua."
        elif remaining_pages == 0:
            dist_text = f"Jokainen tiedosto sisältää {pages_per_file} sivua."
        else:
            dist_text = (
                f"{full_files} tiedostoa sisältää {pages_per_file} sivua, "
                f"viimeinen tiedosto sisältää {remaining_pages} sivua."
            )
        self.page_distribution_info.setText(dist_text)

    def update_page_count(self, page_count: int):
        """Päivittää tiedossa olevan PDF:n kokonaissivumäärän."""
        self.page_count = max(0, page_count)
        if self.page_count > 0:
            self.pages_spinner.setMaximum(self.page_count)
            if self.pages_spinner.value() > self.page_count:
                self.pages_spinner.setValue(self.page_count)
        else:
            self.pages_spinner.setMaximum(1)
        self._update_info_labels()

    def get_pages_per_file(self) -> int:
        """Palauttaa käyttäjän asettaman sivumäärän per tiedosto."""
        return self.pages_spinner.value()
