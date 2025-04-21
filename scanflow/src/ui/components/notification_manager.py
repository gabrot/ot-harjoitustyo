"""
Moduuli ilmoitusten näyttämiseen Scanflow-sovelluksen käyttöliittymässä.

Tarjoaa `NotificationManager`-luokan, joka hallinnoi ilmoitusviestien
näyttämistä ja piilottamista sovellusikkunan yläreunassa käyttäen animaatioita.
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from ui.styles.dialog_styles import DialogStyles


class NotificationManager:
    """
    Hallinnoi ilmoitusviestien näyttämistä ja piilottamista sovellusikkunassa.

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
        """
        Alustaa ilmoitustenhallinnan.

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
        """
        Näyttää ilmoitusviestin määritetyllä tyylillä ja kestolla.

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

        try:
            DialogStyles.apply_notification_style(
                self.notification_container,
                notification_label,
                close_button,
                notification_type
            )
            auto_hide_duration = 0 if notification_type == "error" else duration
        except Exception as e:
            print(f"Virhe ilmoituksen tyylin soveltamisessa: {e}")
            auto_hide_duration = duration

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

    def hide_notification(self):
        """
        Piilottaa ilmoituksen häivytysanimaation avulla.
        """
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
        """
        Sijoittaa ilmoituksen optimaaliseen kohtaan ikkunassa.
        """
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
