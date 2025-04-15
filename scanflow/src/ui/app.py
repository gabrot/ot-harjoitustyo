"""ScanFlow-sovelluksen pääikkuna ja käyttöliittymän logiikka."""

import os
from typing import List, Tuple, Optional, Any
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QApplication,
    QStackedWidget,
    QGroupBox,
    QFileDialog,
    QProgressBar,
)
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot

from ui.styles import QtTheme
from ui.styles.button_styles import SPLIT_BUTTON_STYLE
from ui.styles.group_styles import COMMON_GROUP_BOX_STYLE

from ui.components.drop_area_widget import DropAreaWidget
from ui.components.custom_range_manager import CustomRangeManager
from ui.components.notification_manager import NotificationManager
from ui.components.fixed_range_settings import FixedRangeSettings
from ui.components.file_info_section import FileInfoSection
from ui.components.mode_selector import ModeSelectorGroup

try:
    from services.pdf_splitter_service import PDFSplitterService
except ImportError:
    print(
        "Varoitus: PDFSplitterService-palvelua ei löytynyt. Käytetään dummy-palvelua."
    )

    class PDFSplitterService:
        def get_pdf_info(self, file_path):
            import time

            time.sleep(0.5)
            return {
                "page_count": 10,
                "file_path": file_path,
                "file_name": os.path.basename(file_path),
            }

        def split_by_fixed_range(
            self,
            file_path,
            pages_per_file,
            output_dir,
            base_filename,
            progress_callback=None,
        ):
            total_parts = 3
            parts_done = 0
            for i in range(total_parts):
                import time

                time.sleep(0.7)
                parts_done += 1
                if progress_callback:
                    progress_callback(int(parts_done / total_parts * 100))
            return [
                os.path.join(output_dir, f"{base_filename}_part{i + 1}.pdf")
                for i in range(total_parts)
            ]

        def split_by_custom_ranges(
            self, file_path, ranges, output_dir, base_filename, progress_callback=None
        ):
            total_parts = len(ranges)
            parts_done = 0
            for i in range(total_parts):
                import time

                time.sleep(0.6)
                parts_done += 1
                if progress_callback:
                    progress_callback(int(parts_done / total_parts * 100))
            return [
                os.path.join(output_dir, f"{base_filename}_custom_part{i + 1}.pdf")
                for i in range(total_parts)
            ]


class Worker(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(
        self,
        service: PDFSplitterService,
        mode: int,
        file_path: str,
        output_dir: str,
        base_filename: str,
        settings: Any,
    ):
        super().__init__()
        self.service = service
        self.mode = mode
        self.file_path = file_path
        self.output_dir = output_dir
        self.base_filename = base_filename
        self.settings = settings
        self._is_cancelled = False

    @pyqtSlot()
    def run(self):
        """Suorittaa PDF-tiedoston jakamisen annetun tilan ja asetusten mukaan."""
        try:
            output_files = []
            if self._is_cancelled:
                return

            if self.mode == 0:
                pages_per_file = self.settings
                output_files = self.service.split_by_fixed_range(
                    self.file_path,
                    pages_per_file,
                    self.output_dir,
                    self.base_filename,
                    progress_callback=self.progress.emit,
                )
            else:
                ranges_to_split = self.settings
                output_files = self.service.split_by_custom_ranges(
                    self.file_path,
                    ranges_to_split,
                    self.output_dir,
                    self.base_filename,
                    progress_callback=self.progress.emit,
                )

            if not self._is_cancelled:
                self.finished.emit(output_files)

        except Exception as e:
            if not self._is_cancelled:
                self.error.emit(f"Virhe jakamisessa: {str(e)}")

    def cancel(self):
        """Keskeyttää työn suorittamisen."""
        self._is_cancelled = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_service = PDFSplitterService()
        self.current_file_path: Optional[str] = None
        self.page_count: int = 0
        self.thread: Optional[QThread] = None
        self.worker: Optional[Worker] = None
        self._init_window()
        self._init_ui()

    def _init_window(self):
        """Alustaa pääikkunan asetukset."""
        self.setWindowTitle("ScanFlow PDF-jakaja")
        self.setMinimumSize(600, 750)
        self._setup_window_styles()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        self.main_layout = main_layout

    def _setup_window_styles(self):
        """Asettaa ikkunan tyylit."""
        self.setStyleSheet(QtTheme.get_stylesheet())

    def _init_ui(self):
        """Alustaa käyttöliittymän komponentit."""
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)

        self.notification_manager = NotificationManager(self)
        self.drop_area = DropAreaWidget()
        self.file_info_section = FileInfoSection()
        self.mode_selector = ModeSelectorGroup()
        self._create_settings_area()
        self.progress_bar = QProgressBar()
        self.split_button = QPushButton("Jaa PDF")

        self.drop_area.file_dropped.connect(self._load_pdf)
        self.drop_area.browse_button.clicked.connect(self._browse_file)
        self.file_info_section.file_removed.connect(self._remove_file)
        self.mode_selector.mode_changed.connect(self._on_mode_changed)
        self.split_button.clicked.connect(self._start_split_pdf)

        content_layout.addWidget(self.drop_area)
        content_layout.addWidget(self.file_info_section)
        content_layout.addWidget(self.mode_selector)
        content_layout.addWidget(self.settings_stack)
        content_layout.addWidget(self.progress_bar)
        content_layout.addWidget(self.split_button)
        content_layout.addStretch(1)
        self.main_layout.addWidget(content_container)

        self.split_button.setStyleSheet(SPLIT_BUTTON_STYLE)
        self.split_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Jaetaan... %p%")

    def _create_settings_area(self):
        """Luo asetusten alueen käyttöliittymään."""
        self.settings_stack = QStackedWidget()
        self.fixed_settings = FixedRangeSettings()
        self.settings_stack.addWidget(self.fixed_settings)

        custom_settings_widget = QWidget()
        custom_layout = QVBoxLayout(custom_settings_widget)
        custom_layout.setContentsMargins(0, 0, 0, 0)
        custom_layout.setSpacing(10)
        self.range_manager = CustomRangeManager(
            custom_settings_widget, use_frames=False
        )
        ranges_group = QGroupBox("Sivualueet")
        ranges_group.setStyleSheet(COMMON_GROUP_BOX_STYLE)
        ranges_layout = QVBoxLayout(ranges_group)
        ranges_layout.setContentsMargins(10, 15, 10, 10)
        ranges_layout.addWidget(self.range_manager.get_scroll_area())
        custom_layout.addWidget(ranges_group)
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 5, 0, 0)
        button_layout.addWidget(
            self.range_manager.get_add_button(), alignment=Qt.AlignmentFlag.AlignLeft
        )
        custom_layout.addWidget(button_container)
        custom_layout.addStretch(1)
        self.settings_stack.addWidget(custom_settings_widget)
        self.range_manager.get_add_button().setVisible(False)

    def _browse_file(self):
        """Avaa tiedostoselaimen ja lataa valitun PDF-tiedoston."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Valitse PDF", "", "PDF (*.pdf)"
        )
        if file_path:
            self._load_pdf(file_path)

    def _load_pdf(self, file_path: str):
        """Lataa PDF-tiedoston ja päivittää käyttöliittymän.

        Args:
            file_path: Ladattavan tiedoston polku.
        """
        try:
            self.notification_manager.show_notification("Ladataan...", "info")
            QApplication.processEvents()
            pdf_info = self.pdf_service.get_pdf_info(file_path)
            self.current_file_path = file_path
            self.page_count = pdf_info["page_count"]
            self.file_info_section.update_file_info(
                pdf_info["file_name"], self.page_count
            )
            self.drop_area.shrink_area(True)
            self.fixed_settings.update_page_count(self.page_count)
            self.range_manager.update_page_count(self.page_count)
            self.range_manager.reset()
            self.range_manager.get_add_button().setVisible(True)
            self.split_button.setEnabled(True)
            self.notification_manager.show_notification("Ladattu.", "success")
        except (FileNotFoundError, ValueError) as e:
            self._reset_ui_on_error(f"Latausvirhe: {e}")
        except Exception as e:
            self._reset_ui_on_error(f"Odottamaton virhe latauksessa: {e}")

    def _reset_ui_on_error(self, error_message: str):
        """Palauttaa käyttöliittymän oletustilaan virheen jälkeen.

        Args:
            error_message: Näytettävä virheviesti.
        """
        self.current_file_path = None
        self.page_count = 0
        self.file_info_section.clear()
        self.drop_area.shrink_area(False)
        self.notification_manager.show_notification(error_message, "error")
        self.fixed_settings.update_page_count(0)
        self.range_manager.update_page_count(0)
        self.range_manager.reset()
        self.range_manager.get_add_button().setVisible(False)
        self.split_button.setEnabled(False)
        self._set_ui_enabled(True)

    def _remove_file(self):
        """Poistaa ladatun tiedoston ja palauttaa käyttöliittymän oletustilaan."""
        self._reset_ui_on_error("Tiedosto poistettu.")
        self.notification_manager.hide_notification()

    def _on_mode_changed(self, mode_index: int):
        """Päivittää asetusten alueen valitun tilan mukaan.

        Args:
            mode_index: Valitun tilan indeksi.
        """
        self.settings_stack.setCurrentIndex(mode_index)

    def _start_split_pdf(self):
        """Aloittaa PDF-tiedoston jakamisen."""
        if not self.current_file_path or self.thread is not None:
            return

        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Valitse tallennuskansio",
            os.path.dirname(self.current_file_path or ""),
        )
        if not output_dir:
            return

        mode = self.mode_selector.get_selected_mode()
        settings = None
        base_filename = os.path.splitext(os.path.basename(self.current_file_path))[0]

        try:
            if mode == 0:
                pages_per_file = self.fixed_settings.get_pages_per_file()
                if pages_per_file <= 0:
                    raise ValueError("Sivuja per tiedosto > 0.")
                settings = pages_per_file
            else:
                ranges = self.range_manager.get_ranges()
                if not self._validate_custom_ranges(ranges):
                    return
                settings = ranges

            self._set_ui_enabled(False)
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)

            self.thread = QThread()
            self.worker = Worker(
                self.pdf_service,
                mode,
                self.current_file_path,
                output_dir,
                base_filename,
                settings,
            )
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self._on_split_finished)
            self.worker.error.connect(self._on_split_error)
            self.worker.progress.connect(self._update_progress)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self._split_cleanup)

            self.thread.start()

        except ValueError as e:
            self.notification_manager.show_notification(
                f"Virheelliset asetukset: {e}", "error"
            )
        except Exception as e:
            self.notification_manager.show_notification(
                f"Jakon aloitus epäonnistui: {e}", "error"
            )
            self._set_ui_enabled(True)

    @pyqtSlot(list)
    def _on_split_finished(self, output_files: List[str]):
        """Käsittelee onnistuneen PDF-tiedoston jakamisen.

        Args:
            output_files: Lista luoduista tiedostoista.
        """
        if output_files:
            output_dir = os.path.dirname(output_files[0])
            self.notification_manager.show_notification(
                f"PDF jaettu {len(output_files)} tiedostoon. Tallennettu: {output_dir}",
                "success",
            )
        else:
            self.notification_manager.show_notification(
                "Jako valmis, ei luotu tiedostoja.", "info"
            )
        self._set_ui_enabled(True)
        self.progress_bar.setVisible(False)

    @pyqtSlot(str)
    def _on_split_error(self, error_message: str):
        """Käsittelee virheen PDF-tiedoston jakamisessa.

        Args:
            error_message: Virheviesti.
        """
        self.notification_manager.show_notification(error_message, "error")
        self._set_ui_enabled(True)
        self.progress_bar.setVisible(False)

    @pyqtSlot(int)
    def _update_progress(self, value: int):
        """Päivittää edistymispalkin arvon.

        Args:
            value: Edistymisen prosenttiosuus.
        """
        self.progress_bar.setValue(value)

    def _split_cleanup(self):
        """Siivoaa jakamisen jälkeiset resurssit."""
        self.thread = None
        self.worker = None

    def _validate_custom_ranges(self, ranges: List[Tuple[int, int]]) -> bool:
        """Tarkistaa mukautettujen alueiden kelvollisuuden.

        Args:
            ranges: Lista mukautettuja alueita.

        Returns:
            True, jos alueet ovat kelvollisia, muuten False.
        """
        if not ranges:
            self.notification_manager.show_notification(
                "Määrittele vähintään yksi sivualue.", "error"
            )
            return False
        return True

    def _set_ui_enabled(self, enabled: bool):
        """Asettaa käyttöliittymän komponenttien tilan.

        Args:
            enabled: True, jos käyttöliittymä on käytössä, muuten False.
        """
        self.drop_area.setEnabled(enabled)
        self.file_info_section.setEnabled(enabled)
        self.mode_selector.setEnabled(enabled)
        self.settings_stack.setEnabled(enabled)
        self.split_button.setEnabled(enabled and self.current_file_path is not None)

    def closeEvent(self, event):
        """Varmistaa, että säie lopetetaan kun ikkuna suljetaan."""
        if self.thread and self.thread.isRunning():
            self.worker.cancel()
            self.thread.quit()
            self.thread.wait()
        event.accept()

    def showEvent(self, event):
        """Varmistaa ilmoituksen oikean sijainnin näytölle tullessa.

        Args:
            event: Näyttämistapahtuma.
        """
        super().showEvent(event)
        self.notification_manager.position_notification()

    def resizeEvent(self, event):
        """Varmistaa ilmoituksen oikean sijainnin koon muutoksen jälkeen.

        Args:
            event: Koonmuutostapahtuma.
        """
        super().resizeEvent(event)
        self.notification_manager.position_notification()
