"""Moduuli ilmoitusten näyttämiseen ScanFlow-sovelluksen käyttöliittymässä.

Tarjoaa `NotificationManager`-luokan, joka hallinnoi ilmoitusviestien
näyttämistä ja piilottamista sovellusikkunan yläreunassa käyttäen animaatioita.
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect


class NotificationManager:
    """Hallinnoi ilmoitusviestien näyttämistä ja piilottamista sovellusikkunassa.

    Luo ja hallinnoi QFrame-pohjaista ilmoituspalkkia, joka voidaan näyttää
    eri tyypeillä (info, error, success) ja joka piilotetaan automaattisesti
    tai manuaalisesti.

    Attributes:
        parent_window (QMainWindow): Ikkuna, johon ilmoitukset liitetään.
        notification_container (QFrame | None): Itse ilmoituspalkki-widget.
        fade_out_animation (QPropertyAnimation | None): Animaatio ulospäin häivytykselle.
        hide_timer (QTimer): Ajastin automaattiselle piilotukselle.
    """

    def __init__(self, parent_window):
        """Alustaa ilmoitustenhallinnan.

        Args:
            parent_window (QMainWindow): Ikkuna, johon ilmoituspalkki lisätään.
        """
        self.parent_window = parent_window
        self.notification_container = None
        self.fade_out_animation = None
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_notification)

    def show_notification(self, message, notification_type="info", duration=5000):
        """Näyttää ilmoitusviestin määritetyllä tyylillä ja kestolla.

        Args:
            message (str): Näytettävä viesti.
            notification_type (str): Ilmoituksen tyyppi ('info', 'error', 'success').
                                     Oletus 'info'.
            duration (int): Aika ms, jonka jälkeen ilmoitus piilotetaan (ei error-tyypille).
                            Oletus 5000 ms.
        """
        self.hide_timer.stop()
        if self.notification_container and self.notification_container.isVisible():
            self.notification_container.hide()

        self.notification_container = QFrame(self.parent_window)
        self.notification_container.setObjectName("NotificationOverlay")
        self.notification_container.setCursor(Qt.CursorShape.PointingHandCursor)
        self.notification_container.mousePressEvent = (
            lambda event: self.hide_notification()
        )

        notification_layout = QHBoxLayout(self.notification_container)
        notification_layout.setContentsMargins(15, 8, 10, 8)
        notification_layout.setSpacing(10)

        notification_label = QLabel(message)
        notification_label.setWordWrap(True)
        notification_label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        notification_layout.addWidget(notification_label, stretch=1)

        close_button = QPushButton("×")
        close_button.setFixedSize(24, 24)
        close_button.setToolTip("Sulje ilmoitus")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(self.hide_notification)
        notification_layout.addWidget(
            close_button,
            alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        )

        bg_color, text_color, border_color, close_color = self._get_notification_colors(
            notification_type
        )
        auto_hide_duration = 0 if notification_type == "error" else duration

        self.notification_container.setStyleSheet(
            f"""
            QFrame#NotificationOverlay {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 5px;
            }}
        """
        )
        notification_label.setStyleSheet(
            f"color: {text_color}; font-size: 14px; font-weight: 500; background: transparent; border: none;"
        )
        close_button.setStyleSheet(
            f"""
            QPushButton {{ background: transparent; border: none; color: {close_color}; font-weight: bold; font-size: 20px; padding: 0 0 2px 0; }}
            QPushButton:hover {{ color: #000; }}
        """
        )

        self.position_notification()

        fade_animation = QPropertyAnimation(
            self.notification_container, b"windowOpacity"
        )
        fade_animation.setDuration(250)
        fade_animation.setStartValue(0.0)
        fade_animation.setEndValue(0.95)
        fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.notification_container.setWindowOpacity(0.0)
        self.notification_container.show()
        self.notification_container.raise_()
        fade_animation.start()

        if auto_hide_duration > 0:
            self.hide_timer.start(auto_hide_duration)

    def _get_notification_colors(self, notification_type):
        """Palauttaa värit ilmoitustyypin perusteella.

        Args:
            notification_type (str): 'info', 'error' tai 'success'.

        Returns:
            tuple: (bg_color, text_color, border_color, close_color)
        """
        if notification_type == "error":
            return ("#f8d7da", "#721c24", "#f5c6cb", "#721c24")
        elif notification_type == "success":
            return ("#d4edda", "#155724", "#c3e6cb", "#155724")
        else:
            return ("#e2f3fd", "#004085", "#b8daff", "#004085")

    def hide_notification(self):
        self.hide_timer.stop()
        if (
            self.notification_container
            and self.notification_container.isVisible()
            and (
                not self.fade_out_animation
                or self.fade_out_animation.state() != QPropertyAnimation.State.Running
            )
        ):
            self.fade_out_animation = QPropertyAnimation(
                self.notification_container, b"windowOpacity"
            )
            self.fade_out_animation.setDuration(300)
            self.fade_out_animation.setStartValue(
                self.notification_container.windowOpacity()
            )
            self.fade_out_animation.setEndValue(0.0)
            self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InCubic)
            self.fade_out_animation.finished.connect(self._on_hide_finished)
            self.fade_out_animation.start()

    def _on_hide_finished(self):
        if self.notification_container:
            self.notification_container.hide()

    def position_notification(self):
        if self.notification_container:
            max_width = 600
            side_margin = 20
            available_width = self.parent_window.width() - (2 * side_margin)
            width = min(max_width, available_width)

            self.notification_container.setFixedWidth(width)
            self.notification_container.adjustSize()

            x = (self.parent_window.width() - width) // 2
            y = 15
            self.notification_container.setGeometry(
                QRect(x, y, width, self.notification_container.height())
            )
            self.notification_container.raise_()
