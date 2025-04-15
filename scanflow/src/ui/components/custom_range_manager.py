"""Moduuli mukautettujen PDF-sivualueiden hallintaan käyttöliittymässä."""

from typing import List, Tuple, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QPushButton,
    QLabel,
    QSpinBox,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from ui.styles.button_styles import ADD_RANGE_BUTTON_STYLE

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

class CustomRangeRow(QWidget):
    """Yksittäinen rivi mukautetun sivualueen määrittämiseksi."""

    removed = pyqtSignal(QWidget)

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        page_count: int = 0,
        use_frames: bool = True,
    ):
        """Alustaa uuden sivualuerivin.

        Args:
            parent: Yläkomponentti, johon tämä rivi kuuluu
            page_count: PDF:n sivujen kokonaismäärä
            use_frames: Käytetäänkö kehyksiä tyylittelyssä
        """
        super().__init__(parent)
        self.page_count = page_count
        self.use_frames = use_frames
        self._init_ui()

    def _init_ui(self):
        """Alustaa rivin käyttöliittymäkomponentit ja asettelun."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setStyleSheet("background-color: transparent;")

        self.start_spin = QSpinBox(self)
        self.start_spin.setMinimum(1)
        self.start_spin.setMaximum(max(1, self.page_count))
        self.start_spin.setFixedWidth(60)
        self.start_spin.setStyleSheet(RANGE_INPUT_STYLE)
        self.start_spin.setToolTip("Alueen ensimmäinen sivu")

        self.end_spin = QSpinBox(self)
        self.end_spin.setMinimum(1)
        self.end_spin.setMaximum(max(1, self.page_count))
        self.end_spin.setValue(max(1, self.page_count))
        self.end_spin.setFixedWidth(60)
        self.end_spin.setStyleSheet(RANGE_INPUT_STYLE)
        self.end_spin.setToolTip("Alueen viimeinen sivu")

        page_label = QLabel("Sivut")
        page_label.setFrameStyle(QFrame.Shape.NoFrame)

        dash_label = QLabel("-")
        dash_label.setFrameStyle(QFrame.Shape.NoFrame)

        remove_btn = QPushButton("×")
        remove_btn.setObjectName("DeleteRangeButton")  
        remove_btn.setFixedSize(24, 24) 
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.clicked.connect(self._on_remove_clicked)
        remove_btn.setToolTip("Poista tämä sivualue")
        self.remove_btn = remove_btn

        layout.addWidget(page_label)
        layout.addWidget(self.start_spin)
        layout.addWidget(dash_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.end_spin)
        layout.addStretch(1)
        layout.addWidget(self.remove_btn)

        self.start_spin.valueChanged.connect(self._adjust_end_spin_min)
        self.end_spin.valueChanged.connect(self._adjust_start_spin_max)
        self._adjust_end_spin_min()

    def _adjust_end_spin_min(self):
        """Säätää loppusivun minimiarvoa alkusivun perusteella."""
        self.end_spin.setMinimum(self.start_spin.value())

    def _adjust_start_spin_max(self):
        """Säätää alkusivun maksimiarvoa loppusivun perusteella."""
        self.start_spin.setMaximum(self.end_spin.value())

    def _on_remove_clicked(self):
        """Lähettää 'removed'-signaalin."""
        self.removed.emit(self)

    def get_range(self) -> Optional[Tuple[int, int]]:
        """Palauttaa riville asetetun sivualueen."""
        start = self.start_spin.value()
        end = self.end_spin.value()
        return (start, end) if start <= end else None

    def update_page_count(self, page_count: int):
        """Päivittää spinboxien maksimiarvon."""
        self.page_count = max(0, page_count)
        max_val = max(1, self.page_count)

        current_start = self.start_spin.value()
        current_end = self.end_spin.value()

        self.start_spin.setMaximum(max_val)
        self.end_spin.setMaximum(max_val)

        if current_start > max_val:
            self.start_spin.setValue(max_val)
        if current_end > max_val:
            self.end_spin.setValue(max_val)

        if self.start_spin.value() > self.end_spin.value():
            self.end_spin.setValue(self.start_spin.value())

        self._adjust_end_spin_min()
        self._adjust_start_spin_max()


class CustomRangeManager:
    """Hallinnoi mukautettujen sivualueiden käyttöliittymää."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        page_count: int = 0,
        use_frames: bool = True,
    ):
        """Alustaa sivualueiden hallintakomponentin."""
        self.parent = parent
        self.page_count = page_count
        self.use_frames = use_frames
        self.range_rows: List[CustomRangeRow] = []
        self._init_ui()

    def _init_ui(self):
        """Alustaa managerin käyttöliittymäkomponentit."""
        self.scroll_widget = QWidget(self.parent)
        self.scroll_widget.setStyleSheet("background-color: transparent;")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch(1)

        self.scroll_area = QScrollArea(self.parent)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea { background-color: transparent; border: none; }
            QScrollBar:vertical { background-color: transparent; width: 8px; margin: 0; border-radius: 4px; }
            QScrollBar::handle:vertical { background-color: #cccccc; border-radius: 4px; min-height: 25px; }
            QScrollBar::handle:vertical:hover { background-color: #bbbbbb; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; background: none; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """
        )

        self.add_button = QPushButton("+ Lisää sivualue")
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.setStyleSheet(ADD_RANGE_BUTTON_STYLE)
        self.add_button.clicked.connect(self.add_custom_range)

    def add_custom_range(self):
        """Lisää uuden `CustomRangeRow`-widgetin."""
        stretch_item = self.scroll_layout.takeAt(self.scroll_layout.count() - 1)
        new_row = CustomRangeRow(self.scroll_widget, self.page_count, self.use_frames)
        new_row.removed.connect(self.remove_range_row)
        self.scroll_layout.addWidget(new_row)
        self.range_rows.append(new_row)
        if stretch_item:
            self.scroll_layout.addItem(stretch_item)
        new_row.update_page_count(self.page_count)

    def remove_range_row(self, row: CustomRangeRow):
        """Poistaa annetun `CustomRangeRow`-widgetin."""
        if len(self.range_rows) <= 1:
            return
        if row in self.range_rows:
            self.range_rows.remove(row)
            self.scroll_layout.removeWidget(row)
            row.deleteLater()

    def get_scroll_area(self) -> QScrollArea:
        """Palauttaa QScrollArea-widgetin."""
        return self.scroll_area

    def get_add_button(self) -> QPushButton:
        """Palauttaa 'Lisää sivualue' -painikkeen."""
        return self.add_button

    def get_ranges(self) -> List[Tuple[int, int]]:
        """Palauttaa listan kelvollisista sivualueista."""
        return [rng for row in self.range_rows if (rng := row.get_range()) is not None]

    def update_page_count(self, page_count: int):
        """Päivittää PDF:n sivumäärän ja välittää sen riveille."""
        self.page_count = max(0, page_count)
        for row in self.range_rows:
            row.update_page_count(self.page_count)

    def reset(self):
        """Palauttaa managerin alkutilaan."""
        while len(self.range_rows) > 0:
            row_to_remove = self.range_rows.pop()
            self.scroll_layout.removeWidget(row_to_remove)
            row_to_remove.deleteLater()
        stretch_item = self.scroll_layout.takeAt(self.scroll_layout.count() - 1)
        if stretch_item:
            del stretch_item
        self.scroll_layout.addStretch(1)
        if self.page_count > 0:
            self.add_custom_range()
