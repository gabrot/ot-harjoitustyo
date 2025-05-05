"""
Sovelluksen päämoduuli ja käynnistyspiste.

Alustaa ja käynnistää Scanflow-sovelluksen graafisen käyttöliittymän.
"""

import sys
import os
import logging
import warnings
import tempfile
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

def get_log_file_path():
    """Palauttaa lokitiedoston polun huomioiden ympäristön (kehitys vs. paketoitu)"""
    try:
        user_home = os.path.expanduser("~")
        app_dir = os.path.join(user_home, ".scanflow")
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)
        return os.path.join(app_dir, "scanflow.log")
    except (IOError, PermissionError):
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, "scanflow.log")

def create_file_handler(log_file):
    """Luo tiedostoon kirjoittavan lokikäsittelijän"""
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    return file_handler

def create_console_handler():
    """Luo konsoliin kirjoittavan lokikäsittelijän"""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)
    return console_handler

def setup_file_logger():
    """Alustaa tiedostoon kirjoittavan lokittajan"""
    log_file = get_log_file_path()
    try:
        handler = create_file_handler(log_file)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        if root_logger.hasHandlers():
            root_logger.handlers.clear()
        root_logger.addHandler(handler)
        return root_logger
    except (IOError, PermissionError) as e:
        print(f"Varoitus: Lokitiedoston luonti epäonnistui: {str(e)}")
        handler = create_console_handler()
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        if root_logger.hasHandlers():
            root_logger.handlers.clear()
        root_logger.addHandler(handler)
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

def initialize_logging():
    """Alustaa lokituksen sovellukselle"""
    setup_file_logger()
    logger = setup_console_logger()
    logger.info("Scanflow käynnistetään...")
    logger.info("Lokitiedoston sijainti: %s", get_log_file_path())
    return logger

def initialize_application():
    """Alustaa Qt-sovelluksen"""
    return QtWidgets.QApplication(sys.argv) # pylint: disable=c-extension-no-member

def start_ui(logger):
    """Käynnistää käyttöliittymän ja asettaa virheenkäsittelijät"""
    sys.excepthook = except_hook_factory(logger)
    try:
        pdf_service = get_pdf_service(logger)
        window = MainWindow(pdf_service)
        window.show()
        return window
    except (RuntimeError, ImportError) as e:
        logger.exception("Virhe sovelluksen käynnistyksessä: %s", str(e))
        show_critical_message(
            "Käynnistysvirhe",
            "Sovelluksen käynnistäminen epäonnistui. "
            "Tarkista lokitiedosto lisätietoja varten."
        )
        sys.exit(1)

def main():
    """Sovelluksen pääfunktio"""
    logger = initialize_logging()
    app = initialize_application()
    start_ui(logger)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
