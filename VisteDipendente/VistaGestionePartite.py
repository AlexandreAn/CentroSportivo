from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy

from VisteDipendente.VistaAggiungiPartita import VistaAggiungiPartita
from VisteDipendente.VistaVisualizzaListaPartite import VistaVisualizzaListaPartite


class VistaGestionePartite(QWidget):

    def __init__(self, parent=None):
        super(VistaGestionePartite, self).__init__(parent)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_generic_button("Aggiungi Partita", self.aggiungiPartita), 0, 0)
        grid_layout.addWidget(self.get_generic_button("Visualizza Lista Partite", self.visualizzaListaPartite), 0, 1)
        self.setLayout(grid_layout)
        self.resize(500, 400)
        self.setWindowTitle("Gestione Partite")

    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(on_click) #non gli piace connect
        return button

    def aggiungiPartita(self):
        self.aggiungi_partita = VistaAggiungiPartita()
        self.aggiungi_partita.show()

    def visualizzaListaPartite(self):
        self.lista_partite = VistaVisualizzaListaPartite()
        self.lista_partite.show()
