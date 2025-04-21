"""
Moduuli PDF-dokumentin jakamistilan valintakomponentille.

Tarjoaa `ModeSelectorGroup`-luokan, joka on QGroupBox ja sisältää
radiopainikkeet PDF:n jakamistavan valitsemiseksi: joko kiinteän
sivumäärän mukaan tai mukautettujen sivualueiden perusteella.
"""

from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt6.QtCore import pyqtSignal
from ui.styles.container_styles import ContainerStyles


class ModeSelectorGroup(QGroupBox):
    """
    Ryhmälaatikko PDF-dokumentin jakamistilan valintaan.

    Sisältää kaksi radiopainiketta (`QRadioButton`), joilla käyttäjä voi
    valita haluamansa jakotavan. Lähettää signaalin, kun valinta muuttuu.

    Signals:
        mode_changed (int): Lähetetään, kun valittu tila vaihtuu.
                            Argumentti on 0, jos "Kiinteä jako"
                            valitaan, ja 1, jos "Mukautetut alueet"
                            valitaan.
    """

    mode_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        """
        Alustaa jakamistilan valintaryhmän.

        Args:
            parent (QWidget, optional): Isäntäwidget. Oletus None.
        """
        super().__init__("Jakamistila", parent)
        ContainerStyles.apply_group_box_style(self)
        self._init_ui()

    def _init_ui(self):
        """Alustaa radiopainikkeet ja niiden asettelun."""
        mode_layout = QHBoxLayout(self)
        mode_layout.setSpacing(20)

        self.mode_button_group = QButtonGroup(self)

        self.fixed_radio = QRadioButton("Kiinteä jako")
        self.fixed_radio.setToolTip("Jaa PDF osiin, joissa on sama määrä sivuja.")
        self.fixed_radio.setChecked(True)
        self.fixed_radio.toggled.connect(self._on_mode_toggled)
        mode_layout.addWidget(self.fixed_radio)
        self.mode_button_group.addButton(self.fixed_radio, 0)

        self.custom_radio = QRadioButton("Mukautetut alueet")
        self.custom_radio.setToolTip(
            "Määrittele itse, mitkä sivut tulevat mihinkin tiedostoon."
        )
        self.custom_radio.toggled.connect(self._on_mode_toggled)
        mode_layout.addWidget(self.custom_radio)
        self.mode_button_group.addButton(self.custom_radio, 1)

        mode_layout.addStretch(1)

    def _on_mode_toggled(self, checked):
        """
        Käsittelee radiopainikkeen tilan muutoksen.

        Lähettää `mode_changed`-signaalin vain, kun painike *valitaan*.

        Args:
            checked (bool): Tosi, jos painike on nyt valittu, muuten epätosi.
        """
        if checked:
            selected_id = self.mode_button_group.checkedId()
            if selected_id != -1:
                self.mode_changed.emit(selected_id)

    def get_selected_mode(self):
        """
        Palauttaa tällä hetkellä valitun jakamistilan ID:n.

        Returns:
            int: 0 (Kiinteä jako) tai 1 (Mukautetut alueet).
        """
        return self.mode_button_group.checkedId()
