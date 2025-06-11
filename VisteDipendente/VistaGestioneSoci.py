from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy

from VisteDipendente.VistaAbbonaSocio import VistaAbbonaSocio
from VisteDipendente.VistaConfermaEliminazioneSocio import VistaConfermaEliminazioneSocio
from VisteDipendente.VistaDettagliSocio import VistaDettagliSocio

from VisteDipendente.VistaRicercaSocio import VistaRicercaSocio
from VisteDipendente.VistaVisualizzaListaAbbonamenti import VistaVisualizzaListaAbbonamenti

from VisteDipendente.VistaVisualizzaListaSoci import VistaVisualizzaListaSoci


class VistaGestioneSoci(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneSoci, self).__init__(parent)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_generic_button("Visualizza Lista Soci", self.visualizzaListaSoci), 0, 0)
        grid_layout.addWidget(self.get_generic_button("Visualizza Dati Socio", self.datiSocio), 0, 1)
        grid_layout.addWidget(self.get_generic_button("Elimina Socio", self.eliminaSocio), 1, 0)


        grid_layout.addWidget(self.get_generic_button("Abbona Socio", self.abbonaSocio), 1, 1)  # nuova funzionalità
        grid_layout.addWidget(self.get_generic_button("Visualizza Lista Abbonamenti", self.visualizzaListaAbbonamenti), 2, 0)  # nuova funzionalità



        self.setLayout(grid_layout)
        self.resize(500,400)
        self.setWindowTitle("Gestione Soci")

    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # ridimensionamento finestra e bottone
        button.clicked.connect(on_click)  # non gli piace connect
        return button



    def visualizzaListaSoci(self):
        self.vista_lista_soci = VistaVisualizzaListaSoci()
        self.vista_lista_soci.show()

    def abbonaSocio(self):
        self.vista_abbona_socio = VistaAbbonaSocio()
        self.vista_abbona_socio.show()

    def visualizzaListaAbbonamenti(self):
        from PyQt5.QtWidgets import QMessageBox
        from Abbonamento import Abbonamento
        abbonamenti = Abbonamento.getAbbonamenti()
        if not abbonamenti:
            QMessageBox.information(self, "Nota", "Nessun abbonamento trovato.")
            return

        self.vista_visualizza_abbonamenti = VistaVisualizzaListaAbbonamenti()
        self.vista_visualizza_abbonamenti.show()

    def datiSocio(self):
        def apri_dettagli(socio):
            self.vista_dettagli = VistaDettagliSocio(socio)
            self.vista_dettagli.show()

        self.vista_ricerca = VistaRicercaSocio(on_socio_trovato=apri_dettagli)
        self.vista_ricerca.show()

    def eliminaSocio(self):
        def apri_conferma(socio):
            self.vista_elimina = VistaConfermaEliminazioneSocio(socio)
            self.vista_elimina.show()

        self.vista_ricerca = VistaRicercaSocio(on_socio_trovato=apri_conferma)
        self.vista_ricerca.show()
