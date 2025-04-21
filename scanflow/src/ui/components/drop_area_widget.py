"""
Moduuli PDF-tiedostojen raahaus- ja pudotusalueen komponentille.

Tarjoaa graafisen käyttöliittymäkomponentin (DropAreaWidget), johon
käyttäjä voi raahata ja pudottaa PDF-tiedostoja tai valita tiedoston
painikkeen kautta. Komponentti muuttaa ulkoasuaan tiedoston latauksen
ja raahauksen aikana.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent
from ui.styles.container_styles import ContainerStyles
from ui.styles.button_styles import ButtonStyles


class DropAreaWidget(QFrame):
    """
    Widget PDF-tiedostojen raahaamista ja valitsemista varten.

    Tämä QFrame-pohjainen widget hyväksyy pudotetut tiedostot, tarkistaa
    niiden olevan PDF-muotoisia ja lähettää signaalin, kun kelvollinen
    tiedosto on pudotettu tai valittu. Se myös muuttaa visuaalista
    ilmettään tiedoston latauksen ja raahauksen aikana.

    Attributes:
        file_dropped: Signaali, joka lähetetään, kun kelvollinen PDF-tiedosto
                      on pudotettu tai valittu. Argumenttina on tiedoston polku.
    """

    file_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Alustaa DropAreaWidgetin.

        Args:
            parent: Isäntäwidget. Oletus None.
        """
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        ContainerStyles.apply_drop_area_normal_style(self)
        self._normal_height = 240
        self._shrunk_height = 80
        self.setMinimumHeight(self._normal_height)
        self._file_loaded = False
        self._init_ui()

    def _init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        self._setup_expanded_ui()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _clear_layout(self):
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                layout = item.layout()
                if layout:
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget:
                            sub_widget.deleteLater()
                    layout.deleteLater()
                del item

    def _setup_expanded_ui(self):
        """Rakentaa laajennetun (oletus) käyttöliittymän."""
        self._clear_layout()
        self.setMinimumHeight(self._normal_height)
        self.main_layout.setContentsMargins(20, 40, 20, 20)
        self._file_loaded = False

        drop_label = QLabel("Vedä ja pudota PDF-tiedosto tähän")
        drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ContainerStyles.apply_drop_label_style(drop_label)
        self.main_layout.addWidget(drop_label)

        or_label = QLabel("- tai -")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ContainerStyles.apply_or_label_style(or_label)
        self.main_layout.addWidget(or_label)

        self.browse_button = QPushButton("Valitse tiedosto")
        ButtonStyles.apply_browse_button_style(self.browse_button)
        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_button.setFixedWidth(150)
        self.main_layout.addWidget(
            self.browse_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def _setup_shrunk_ui(self):
        """Rakentaa kutistetun käyttöliittymän tiedoston latauksen jälkeen."""
        self._clear_layout()
        self.setMinimumHeight(self._shrunk_height)
        self.main_layout.setContentsMargins(10, 5, 10, 5)
        self._file_loaded = True

        h_container = QWidget()
        h_layout = QHBoxLayout(h_container)
        h_layout.setContentsMargins(5, 0, 5, 0)
        h_layout.setSpacing(10)

        drop_label = QLabel("Tuo uusi PDF-tiedosto")
        ContainerStyles.apply_shrunk_drop_label_style(drop_label)
        drop_label.setWordWrap(True)
        drop_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        drop_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        or_label = QLabel("- tai -")
        ContainerStyles.apply_shrunk_or_label_style(or_label)
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.browse_button = QPushButton("Valitse tiedosto")
        ButtonStyles.apply_browse_button_style(self.browse_button)
        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_button.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        h_layout.addWidget(drop_label, 1)
        h_layout.addWidget(or_label, 0)
        h_layout.addWidget(self.browse_button, 0)

        self.main_layout.addWidget(h_container, alignment=Qt.AlignmentFlag.AlignCenter)

    def shrink_area(self, shrink=True):
        """
        Vaihtaa käyttöliittymän laajennetun ja kutistetun tilan välillä.

        Args:
            shrink: True kutistaa alueen, False laajentaa sen.
        """
        if shrink and not self._file_loaded:
            self._setup_shrunk_ui()
        elif not shrink and self._file_loaded:
            self._setup_expanded_ui()

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Käsittelee, kun tiedosto raahataan widgetin päälle.

        Args:
            event: Raahauksen aloitustapahtuma.
        """
        if event.mimeData().hasUrls() and self._is_valid_drop(event.mimeData()):
            ContainerStyles.apply_drop_area_drag_over_style(self)
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """
        Käsittelee, kun raahaus poistuu widgetin päältä.

        Args:
            event: Raahauksen poistumistapahtuma.
        """
        ContainerStyles.apply_drop_area_normal_style(self)

    def dropEvent(self, event: QDropEvent):
        """
        Käsittelee, kun tiedosto pudotetaan widgetin päälle.

        Args:
            event: Pudotustapahtuma.
        """
        ContainerStyles.apply_drop_area_normal_style(self)
        if event.mimeData().hasUrls() and self._is_valid_drop(event.mimeData()):
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.file_dropped.emit(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event: QMouseEvent):
        """
        Käsittelee hiiren klikkauksen widgetin päällä.

        Args:
            event: Hiiren klikkaustapahtuma.
        """
        super().mousePressEvent(event)

    def _is_valid_drop(self, mime_data: QMimeData):
        """
        Tarkistaa, onko annettu MIME-data kelvollinen pudotus (yksi PDF).

        Args:
            mime_data (QMimeData): Tarkistettava MIME-data.

        Returns:
            bool: True jos data sisältää yhden paikallisen PDF-tiedoston URL:n, muuten False.
        """
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            url = mime_data.urls()[0]
            if url.isLocalFile():
                file_path = url.toLocalFile()
                return file_path.lower().endswith(".pdf")
        return False
