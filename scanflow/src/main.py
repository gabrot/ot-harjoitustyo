"""
Sovelluksen päämoduuli ja käynnistyspiste.

Alustaa ja käynnistää Scanflow-sovelluksen graafisen käyttöliittymän.
"""

import sys
import os
import logging
import warnings
from PyQt6 import QtWidgets
from src.ui.app import MainWindow
from src.services.fallback_pdf_service import FallbackPDFService
from src.services.pdf_splitter_service import PDFSplitterService

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=".*SwigPyPacked.*__module__.*"
)
warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=".*SwigPyObject.*__module__.*"
)
warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message=".*swigvarlink.*__module__.*"
)

def get_pdf_service(logger):
    try:
        PDFSplitterService()
        logger.info("Käytetään varsinaista PDF-palvelua")
        return PDFSplitterService()
    except ImportError:
        logger.info("Käytetään fallback-palvelua, koska varsinainen palvelu ei ole saatavilla")
        return FallbackPDFService()

def setup_file_logger():
    log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(log_dir, "scanflow.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    return root_logger

def setup_console_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger

def show_critical_message(title, text):
    QtWidgets.QMessageBox.critical(None, title, text) # pylint: disable=c-extension-no-member

def except_hook_factory(logger):
    def except_hook(exc_class, exception, exc_traceback):
        logger.critical(
            "Kriittinen virhe sovelluksessa:",
            exc_info=(exc_class, exception, exc_traceback),
        )
        show_critical_message(
            "Virhe",
            "Sovelluksessa tapahtui odottamaton virhe. "
            "Tarkemmat tiedot löytyvät lokitiedostosta."
        )
    return except_hook

def main():
    setup_file_logger()
    logger = setup_console_logger()
    logger.info("Scanflow käynnistetään...")

    app = QtWidgets.QApplication(sys.argv) # pylint: disable=c-extension-no-member
    sys.excepthook = except_hook_factory(logger)

    try:
        pdf_service = get_pdf_service(logger)
        window = MainWindow(pdf_service)
        window.show()
        sys.exit(app.exec())
    except (RuntimeError, ImportError):
        logger.exception("Virhe sovelluksen käynnistyksessä")
        show_critical_message(
            "Käynnistysvirhe",
            "Sovelluksen käynnistäminen epäonnistui. "
            "Tarkista lokitiedosto lisätietoja varten."
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
