from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from VisteAmministratore.VistaAltreStatistiche import VistaAltreStatistiche
from VisteAmministratore.VistaGraficoPrenotazioni import VistaGraficoPrenotazioni
from VisteAmministratore.VistaGuadagnoPartite import VistaGuadagnoPartite
from VisteAmministratore.VistaPartitePrenotate import VistaPartitePrenotate


class VistaStatistiche(QWidget):
    def __init__(self, parent=None):
        super(VistaStatistiche, self).__init__(parent)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_generic_button("Prenotazioni per fasce orarie", self.visualizzaAbbonamenti), 0, 0)
        grid_layout.addWidget(self.get_generic_button("Guadagno totale", self.visualizzaGuadagnoTotale), 0, 1)
        grid_layout.addWidget(self.get_generic_button("Partite prenotate", self.visualizzaPartitePrenotate), 1, 0)
        grid_layout.addWidget(self.get_generic_button("Altre statistiche", self.visualizzaAltreStatistiche), 1, 1)

        self.setLayout(grid_layout)
        self.resize(500, 400)
        self.setWindowTitle("Visualizza statistiche")

    def visualizzaAltreStatistiche(self):
        self.altreStatistiche = VistaAltreStatistiche()
        self.altreStatistiche.show()

    def visualizzaGuadagnoTotale(self):
        self.guadagnoPartite = VistaGuadagnoPartite()
        self.guadagnoPartite.show()

    def visualizzaPartitePrenotate(self):
        self.partitePrenotate = VistaPartitePrenotate()
        self.partitePrenotate.show()
    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        button.clicked.connect(on_click)
        return button

    def visualizzaAbbonamenti(self):
        self.finestraFasceOrarie = VistaGraficoPrenotazioni()
        self.finestraFasceOrarie.show()
