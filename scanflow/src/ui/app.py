"""
Scanflow-sovelluksen pääikkuna ja käyttöliittymän logiikka.

Tämä moduuli sisältää sovelluksen päänäkymän (MainWindow) sekä
Worker-luokan PDF-tiedostojen käsittelyä varten taustasäikeessä.
"""

import os
import logging
from typing import List, Tuple, Optional, Any
from PyQt6.QtWidgets import ( 
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QApplication,
    QStackedWidget,
    QGroupBox,
    QFileDialog,
    QProgressBar,
    QLineEdit,
    QSizePolicy,
    QScrollArea,
) # pylint: disable=no-name-in-module
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot 
from src.ui.styles import BaseStyles, ButtonStyles, ContainerStyles, DialogStyles, QtTheme
from src.ui.components.drop_area_widget import DropAreaWidget
from src.ui.components.custom_range_manager import CustomRangeManager
from src.ui.components.notification_manager import NotificationManager
from src.ui.components.fixed_range_settings import FixedRangeSettings
from src.ui.components.file_info_section import FileInfoSection
from src.ui.components.mode_selector import ModeSelectorGroup

logger = logging.getLogger(__name__)

class Worker(QObject):
    """
    Suorittaa PDF-tiedoston jakamisen taustasäikeessä.

    Args:
        service: PDF-käsittelypalvelu.
        mode: Käyttötila (0 = kiinteä jako, 1 = mukautettu jako).
        file_path: PDF-tiedoston polku.
        output_dir: Tallennuskansion polku.
        base_filename: Tiedostojen nimen perusosa.
        settings: Jakamisasetukset.
    """
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, service, mode: int, file_path: str, output_dir: str, base_filename: str, settings: Any):
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
        """
        Suorittaa PDF-tiedoston jakamisen valitulla tilalla ja asetuksilla.
        """
        try:
            output_files = []
            if self._is_cancelled:
                return
            if self.mode == 0:
                pages_per_file = self.settings
                try:
                    output_files = self.service.split_by_fixed_range(
                        self.file_path,
                        pages_per_file,
                        self.output_dir,
                        base_filename=self.base_filename,
                        progress_callback=self.progress.emit,
                    )
                except FileNotFoundError:
                    if not self._is_cancelled:
                        self.error.emit(
                            "Tiedostoa ei löydy. Tarkista että tiedosto on vielä saatavilla."
                        )
                    return
                except ValueError as e:
                    if not self._is_cancelled:
                        self.error.emit(f"Jakaminen epäonnistui: {str(e)}")
                    return
                except IOError as e:
                    if not self._is_cancelled:
                        self.error.emit(
                            f"Tiedoston käsittelyssä tapahtui virhe: {str(e)}"
                        )
                    return
                except Exception as e:
                    logger.error("Odottamaton virhe jakaessa PDF-tiedostoa: %s", str(e), exc_info=True)
                    if not self._is_cancelled:
                        self.error.emit(
                            "Odottamaton virhe PDF-tiedoston jakamisessa. Tarkista loki lisätietoja varten."
                        )
                    return
            else:
                ranges_to_split = self.settings
                try:
                    output_files = self.service.split_by_custom_ranges(
                        self.file_path,
                        ranges_to_split,
                        self.output_dir,
                        base_filename=self.base_filename,
                        progress_callback=self.progress.emit,
                    )
                except FileNotFoundError:
                    if not self._is_cancelled:
                        self.error.emit(
                            "Tiedostoa ei löydy. Tarkista että tiedosto on vielä saatavilla."
                        )
                    return
                except ValueError as e:
                    if not self._is_cancelled:
                        self.error.emit(f"Jakaminen epäonnistui: {str(e)}")
                    return
                except IOError as e:
                    if not self._is_cancelled:
                        self.error.emit(
                            f"Tiedoston käsittelyssä tapahtui virhe: {str(e)}"
                        )
                    return
                except Exception as e:
                    logger.error("Odottamaton virhe jakaessa PDF-tiedostoa: %s", str(e), exc_info=True)
                    if not self._is_cancelled:
                        self.error.emit(
                            "Odottamaton virhe PDF-tiedoston jakamisessa. Tarkista loki lisätietoja varten."
                        )
                    return
            if not self._is_cancelled:
                self.finished.emit(output_files)
        except Exception as e:
            logger.error("Kriittinen virhe PDF:n jakamisessa Workerissa: %s", str(e), exc_info=True)
            if not self._is_cancelled:
                self.error.emit(
                    "Virhe PDF:n jakamisessa. Tarkista loki lisätietoja varten."
                )

    def cancel(self):
        """
        Keskeyttää työn suorittamisen.
        """
        self._is_cancelled = True

class MainWindow(QMainWindow):
    """
    Sovelluksen pääikkuna PDF-tiedostojen jakamiseen.

    Args:
        pdf_service: PDF-käsittelypalvelu.
    """
    def __init__(self, pdf_service):
        super().__init__()
        self.pdf_service = pdf_service
        self.current_file_path: Optional[str] = None
        self.page_count: int = 0
        self.thread: Optional[QThread] = None
        self.worker: Optional[Worker] = None
        self.last_save_directory: Optional[str] = None
        self._init_window()
        self._init_ui()
        self._set_ui_enabled(False)
        self._update_split_button_state()

    def _init_window(self):
        self.setWindowTitle("Scanflow - PDF-jakaja")
        self.setMinimumSize(500, 500)
        self._setup_window_styles()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(scroll_area.Shape.NoFrame)
        
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(25)
        
        scroll_area.setWidget(content_widget)
        self.setCentralWidget(scroll_area)
        self.main_layout = main_layout
        self._adjust_initial_size()

    def _adjust_initial_size(self):
        screen = QApplication.primaryScreen().availableGeometry()
        max_width = int(screen.width() * 0.8)
        max_height = int(screen.height() * 0.9)
        width = min(650, max_width)
        height = min(860, max_height)
        self.resize(width, height)

    def _setup_window_styles(self):
        self.setStyleSheet(QtTheme.get_stylesheet())

    def _init_ui(self):
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)

        self.notification_manager = NotificationManager(self)
        self.drop_area = DropAreaWidget()
        self.file_info_section = FileInfoSection()
        self.mode_selector = ModeSelectorGroup()
        self._create_settings_area()
        self._create_output_directory_area()
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
        content_layout.addWidget(self.output_group)
        content_layout.addWidget(self.progress_bar)
        content_layout.addWidget(self.split_button)
        content_layout.addStretch(1)
        self.main_layout.addWidget(content_container)

        ButtonStyles.apply_primary_style(self.split_button)
        self.split_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Jaetaan... %p%")

    def _create_settings_area(self):
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
        ContainerStyles.apply_group_box_style(ranges_group)
        ranges_group.setMinimumHeight(200)
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

    def _create_output_directory_area(self):
        self.output_group = QGroupBox("Tallennuskansio")
        ContainerStyles.apply_group_box_style(self.output_group)
        output_layout = QHBoxLayout(self.output_group)
        output_layout.setContentsMargins(10, 10, 10, 10)
        output_layout.setSpacing(10)

        self.output_dir_line_edit = QLineEdit()
        self.output_dir_line_edit.setPlaceholderText("Valitse tallennuskansio")
        self.output_dir_line_edit.setReadOnly(True)
        self.output_dir_line_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.browse_output_button = QPushButton("Selaa")
        ButtonStyles.apply_browse_output_style(self.browse_output_button)
        self.browse_output_button.clicked.connect(self._browse_output_directory)

        output_layout.addWidget(self.output_dir_line_edit, 1)
        output_layout.addWidget(self.browse_output_button, 0)

    def _browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Valitse PDF", "", "PDF (*.pdf)"
        )
        if file_path:
            self._load_pdf(file_path)

    def _browse_output_directory(self):
        start_directory = self.last_save_directory or os.path.expanduser("~")
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Valitse tallennuskansio",
            start_directory,
        )
        if output_dir:
            self.last_save_directory = output_dir
            self.output_dir_line_edit.setText(output_dir)
            self._update_split_button_state()

    def _update_split_button_state(self):
        enabled = bool(self.current_file_path and self.last_save_directory)
        self.split_button.setEnabled(enabled)

    def _load_pdf(self, file_path: str):
        if self.thread and self.thread.isRunning():
            self.worker.cancel()
            self.thread.quit()
            self.thread.wait()
        self.thread = None
        self.worker = None
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
            self.drop_area.browse_button.clicked.connect(self._browse_file)
            
            self.fixed_settings.update_page_count(self.page_count)
            self.range_manager.update_page_count(self.page_count)
            self.range_manager.reset()
            self.range_manager.get_add_button().setVisible(True)

            if self.current_file_path and not self.output_dir_line_edit.text():
                default_output_dir = os.path.dirname(self.current_file_path)
                self.last_save_directory = default_output_dir
                self.output_dir_line_edit.setText(default_output_dir)
                self._update_split_button_state()

            self._set_ui_enabled(True)
            self.notification_manager.show_notification("Tiedosto ladattu.", "success")
        except FileNotFoundError:
            logger.exception("Tiedostoa ei löydy")
            self._reset_ui_on_error("Tiedostoa ei löydy. Tarkista tiedoston sijainti.")
        except ValueError:
            logger.exception("Virheellinen arvo PDF:n latauksessa")
            self._reset_ui_on_error(
                "PDF-tiedoston lataus epäonnistui. Tiedosto saattaa olla virheellinen."
            )
        except Exception:
            logger.exception("Odottamaton virhe PDF:n latauksessa")
            self._reset_ui_on_error(
                "Odottamaton virhe PDF:n latauksessa. Tarkista loki lisätietoja varten."
            )

    def _reset_ui_on_error(self, error_message: str):
        self.current_file_path = None
        self.page_count = 0
        self.file_info_section.clear()
        self.drop_area.shrink_area(False)
        self.notification_manager.show_notification(error_message, "error")
        self.fixed_settings.update_page_count(0)
        self.range_manager.update_page_count(0)
        self.range_manager.reset()
        self.range_manager.get_add_button().setVisible(False)
        self._set_ui_enabled(False)

        if self.thread and self.thread.isRunning():
            self.worker.cancel()
            self.thread.quit()
            self.thread.wait()
        self.thread = None
        self.worker = None

    def _remove_file(self):
        self._reset_ui_on_error("Tiedosto poistettu.")
        self.notification_manager.hide_notification()
        self.output_dir_line_edit.clear()
        self._update_split_button_state()
        
        try:
            self.drop_area.browse_button.clicked.disconnect(self._browse_file)
        except TypeError:
            pass
            
        self.drop_area.browse_button.clicked.connect(self._browse_file)

    def _on_mode_changed(self, mode_index: int):
        self.settings_stack.setCurrentIndex(mode_index)

    def _start_split_pdf(self):
        output_dir = self.output_dir_line_edit.text()

        if not self.current_file_path or not output_dir or self.thread is not None:
            if self.current_file_path and not output_dir:
                self.notification_manager.show_notification(
                    "Valitse tallennuskansio ennen jakamista.", "warning"
                )
            return

        mode = self.mode_selector.get_selected_mode()
        settings = None
        base_filename = os.path.splitext(os.path.basename(self.current_file_path))[0]

        try:
            if mode == 0:
                pages_per_file = self.fixed_settings.get_pages_per_file()
                if pages_per_file <= 0:
                    raise ValueError("Sivuja per tiedosto tulee olla enemmän kuin 0.")
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
            logger.exception("Virheelliset asetukset")
            self.notification_manager.show_notification(
                "Virheelliset asetukset. Tarkista syöttämäsi arvot.", "error"
            )
        except Exception:
            logger.exception("Odottamaton virhe jaon aloituksessa")
            self.notification_manager.show_notification(
                "Jaon aloitus epäonnistui odottamattoman virheen vuoksi.", "error"
            )
            self._set_ui_enabled(True)
            self.progress_bar.setVisible(False)

    @pyqtSlot(list)
    def _on_split_finished(self, output_files: List[str]):
        if output_files:
            output_dir = os.path.dirname(output_files[0])
            self.notification_manager.show_notification(
                f"PDF jaettu {len(output_files)} tiedostoon. Tiedosto tallennettu: {output_dir}",
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
        self.notification_manager.show_notification(error_message, "error")
        self._set_ui_enabled(True)
        self.progress_bar.setVisible(False)

    @pyqtSlot(int)
    def _update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def _split_cleanup(self):
        self.thread = None
        self.worker = None

    def _validate_custom_ranges(self, ranges: List[Tuple[int, int]]) -> bool:
        if not ranges:
            self.notification_manager.show_notification(
                "Määrittele vähintään yksi sivualue.", "error"
            )
            return False
        return True

    def _set_ui_enabled(self, enabled: bool):
        self.drop_area.setEnabled(True)
        self.file_info_section.setEnabled(enabled)
        self.mode_selector.setEnabled(enabled)
        self.settings_stack.setEnabled(enabled)
        self.output_group.setEnabled(True)
        self._update_split_button_state()

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.worker.cancel()
            self.thread.quit()
            self.thread.wait()
        event.accept()

    def showEvent(self, event):
        super().showEvent(event)
        self.notification_manager.position_notification()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.notification_manager.position_notification()
