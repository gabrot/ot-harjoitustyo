"""Moduuli PDF-tiedostojen raahaus- ja pudotusalueen komponentille.

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
)
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent
from ui.styles.drop_area_styles import (
    DROP_AREA_NORMAL_STYLE,
    DROP_AREA_DRAG_OVER_STYLE,
    DROP_LABEL_STYLE,
    OR_LABEL_STYLE,
    SHRUNK_DROP_LABEL_STYLE,
    SHRUNK_OR_LABEL_STYLE,
)


class DropAreaWidget(QFrame):
    """Widget PDF-tiedostojen raahaamista ja valitsemista varten.

    Tämä QFrame-pohjainen widget hyväksyy pudotetut tiedostot, tarkistaa
    niiden olevan PDF-muotoisia ja lähettää signaalin, kun kelvollinen
    tiedosto on pudotettu tai valittu. Se myös muuttaa visuaalista
    ilmettään tiedoston latauksen ja raahauksen aikana.

    Signals:
        file_dropped (str): Lähetetään, kun kelvollinen PDF-tiedosto
                            on pudotettu tai valittu. Argumenttina on
                            tiedoston polku.
    """

    file_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        """Alustaa DropAreaWidgetin.

        Args:
            parent (QWidget, optional): Isäntäwidget. Oletus None.
        """
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setStyleSheet(DROP_AREA_NORMAL_STYLE)
        self._normal_height = 240
        self._shrunk_height = 80
        self.setMinimumHeight(self._normal_height)
        self._file_loaded = False
        self._init_ui()

    def _init_ui(self):
        """Alustaa widgetin sisäiset käyttöliittymäkomponentit."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self._setup_expanded_ui()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _clear_layout(self):
        """Tyhjentää nykyisen asettelun sisällön."""
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
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self._file_loaded = False

        drop_label = QLabel("Vedä ja pudota PDF-tiedosto tähän")
        drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_label.setStyleSheet(DROP_LABEL_STYLE)
        self.main_layout.addWidget(drop_label)

        or_label = QLabel("- tai -")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        or_label.setStyleSheet(OR_LABEL_STYLE)
        self.main_layout.addWidget(or_label)

        self.browse_button = QPushButton("Valitse tiedosto")
        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_button.setFixedWidth(150)
        self.main_layout.addWidget(
            self.browse_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def _setup_shrunk_ui(self):
        """Rakentaa kutistetun käyttöliittymän tiedoston latauksen jälkeen."""
        self._clear_layout()
        self.setMinimumHeight(self._shrunk_height)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self._file_loaded = True

        h_container = QWidget()
        h_layout = QHBoxLayout(h_container)
        h_layout.setContentsMargins(10, 0, 10, 0)
        h_layout.setSpacing(15)
        h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        drop_label = QLabel("Tuo uusi PDF-tiedosto")
        drop_label.setStyleSheet(SHRUNK_DROP_LABEL_STYLE)
        drop_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        h_layout.addWidget(drop_label)

        or_label = QLabel("- tai -")
        or_label.setStyleSheet(SHRUNK_OR_LABEL_STYLE)
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(or_label)

        self.browse_button = QPushButton("Valitse tiedosto")
        self.browse_button.setFixedWidth(150)
        self.browse_button.setCursor(Qt.CursorShape.PointingHandCursor)
        h_layout.addWidget(self.browse_button)

        self.main_layout.addWidget(h_container)

    def shrink_area(self, shrink=True):
        """Vaihtaa käyttöliittymän laajennetun ja kutistetun tilan välillä.

        Args:
            shrink (bool): True kutistaa alueen, False laajentaa sen.
        """
        if shrink and not self._file_loaded:
            self._setup_shrunk_ui()
        elif not shrink and self._file_loaded:
            self._setup_expanded_ui()

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Käsittelee, kun tiedosto raahataan widgetin päälle.

        Hyväksyy tapahtuman ja muuttaa tyyliä, jos raahattava data
        sisältää yhden kelvollisen PDF-tiedoston.

        Args:
            event (QDragEnterEvent): Raahauksen aloitustapahtuma.
        """
        if event.mimeData().hasUrls() and self._is_valid_drop(event.mimeData()):
            self.setStyleSheet(DROP_AREA_DRAG_OVER_STYLE)
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """Käsittelee, kun raahaus poistuu widgetin päältä.

        Palauttaa oletustyylin.

        Args:
            event (QDragLeaveEvent): Raahauksen poistumistapahtuma.
        """
        self.setStyleSheet(DROP_AREA_NORMAL_STYLE)

    def dropEvent(self, event: QDropEvent):
        """Käsittelee, kun tiedosto pudotetaan widgetin päälle.

        Jos pudotettu tiedosto on kelvollinen PDF, lähettää 'file_dropped'
        signaalin tiedostopolun kanssa ja palauttaa oletustyylin.

        Args:
            event (QDropEvent): Pudotustapahtuma.
        """
        self.setStyleSheet(DROP_AREA_NORMAL_STYLE)
        if event.mimeData().hasUrls() and self._is_valid_drop(event.mimeData()):
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.file_dropped.emit(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event: QMouseEvent):
        """Käsittelee hiiren klikkauksen widgetin päällä.

        Kutsuu `_browse_file`-metodia, jos klikataan.

        Args:
            event (QMouseEvent): Hiiren klikkaustapahtuma.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._browse_file()
        super().mousePressEvent(event)

    def _is_valid_drop(self, mime_data: QMimeData):
        """Tarkistaa, onko annettu MIME-data kelvollinen pudotus (yksi PDF).

        Args:
            mime_data (QMimeData): Tarkistettava MIME-data.

        Returns:
            bool: True, jos data sisältää täsmälleen yhden paikallisen
                  PDF-tiedoston URL:n, muuten False.
        """
        if mime_data.hasUrls() and len(mime_data.urls()) == 1:
            url = mime_data.urls()[0]
            if url.isLocalFile():
                file_path = url.toLocalFile()
                return file_path.lower().endswith(".pdf")
        return False

    def _browse_file(self):
        """Avaa tiedostonvalintaikkunan PDF-tiedoston valitsemiseksi.

        Metodia kutsutaan mousePressEvent-käsittelijässä, mutta toteutus
        on tarkoituksella tyhjä, koska sen käsittely tapahtuu ylemmässä komponentissa.
        """
        pass
