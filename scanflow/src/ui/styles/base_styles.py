"""
Sovelluksen perustyylimäärittelyt.

Tämä moduuli sisältää `BaseStyles`-luokan, joka määrittelee sovelluksen
yhteiset värit, fontit ja muut tyylimäärittelyt.
"""


class BaseStyles:
    """
    Perustyylimäärittelyjen luokka.

    Sisältää vakioita väreille, fonteille, reunuksille ja muille tyylimäärittelyille,
    joita käytetään läpi sovelluksen. Tämän luokan avulla voidaan helposti muuttaa
    sovelluksen ulkoasua keskitetysti.
    """

    PRIMARY = "#ec5f5f"
    PRIMARY_HOVER = "#f98b8b"
    PRIMARY_PRESSED = "#d85050"
    SUCCESS = "#28a745"
    ERROR = "#e74c3c"
    WARNING = "#f39c12"
    INFO = "#3498db"
    BACKGROUND = "#f8f9fa"
    CARD_BG = "#ffffff"
    TEXT_PRIMARY = "#444444"
    TEXT_SECONDARY = "#777777"
    TEXT_LIGHT = "#ffffff"
    TEXT_DARK = "#000000"
    BORDER = "#dddddd"
    BORDER_LIGHT = "#eeeeee"
    DISABLED_BG = "#cccccc"
    DISABLED_TEXT = "#888888"

    NOTIFICATION_ERROR_BG = "#f8d7da"
    NOTIFICATION_ERROR_TEXT = "#721c24"
    NOTIFICATION_ERROR_BORDER = "#f5c6cb"

    NOTIFICATION_SUCCESS_BG = "#d4edda"
    NOTIFICATION_SUCCESS_TEXT = "#155724"
    NOTIFICATION_SUCCESS_BORDER = "#c3e6cb"

    NOTIFICATION_INFO_BG = "#e2f3fd"
    NOTIFICATION_INFO_TEXT = "#004085"
    NOTIFICATION_INFO_BORDER = "#b8daff"

    FONT_SIZE_SMALL = "12px"
    FONT_SIZE_NORMAL = "14px"
    FONT_SIZE_MEDIUM = "15px"
    FONT_SIZE_LARGE = "16px"
    FONT_SIZE_XLARGE = "18px"

    FONT_WEIGHT_NORMAL = "normal"
    FONT_WEIGHT_MEDIUM = "500"
    FONT_WEIGHT_BOLD = "bold"

    BORDER_RADIUS_SMALL = "3px"
    BORDER_RADIUS_NORMAL = "5px"
    BORDER_RADIUS_MEDIUM = "6px"
    BORDER_RADIUS_LARGE = "8px"
    BORDER_RADIUS_XLARGE = "10px"

    PADDING_SMALL = "5px"
    PADDING_MEDIUM = "10px"
    PADDING_LARGE = "20px"

    @classmethod
    def get_notification_colors(cls, notification_type):
        """
        Palauttaa ilmoituksen värit tyypin perusteella.

        Args:
            notification_type (str): Ilmoitustyyppi ('error', 'success' tai 'info').

        Returns:
            tuple: Sisältää taustavärin, tekstivärin, reunavärin ja
                   sulkunapin värin.
        """
        notification_types = {
            "error": (
                cls.NOTIFICATION_ERROR_BG,
                cls.NOTIFICATION_ERROR_TEXT,
                cls.NOTIFICATION_ERROR_BORDER,
                cls.NOTIFICATION_ERROR_TEXT,
            ),
            "success": (
                cls.NOTIFICATION_SUCCESS_BG,
                cls.NOTIFICATION_SUCCESS_TEXT,
                cls.NOTIFICATION_SUCCESS_BORDER,
                cls.NOTIFICATION_SUCCESS_TEXT,
            ),
            "info": (
                cls.NOTIFICATION_INFO_BG,
                cls.NOTIFICATION_INFO_TEXT,
                cls.NOTIFICATION_INFO_BORDER,
                cls.NOTIFICATION_INFO_TEXT,
            ),
        }

        return notification_types.get(notification_type, notification_types["info"])