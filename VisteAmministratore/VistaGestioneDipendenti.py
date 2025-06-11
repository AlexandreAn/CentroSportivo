from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy
from VisteAmministratore.VistaAggiungiDipendente import VistaAggiungiDipendente
from VisteAmministratore.VistaConfermaEliminazioneDipendente import VistaConfermaEliminazioneDipendente
from VisteAmministratore.VistaDettagliDipendente import VistaDettagliDipendente
from VisteAmministratore.VistaListaDipendenti import VistaListaDipendenti
from VisteAmministratore.VistaModificaDipendente import VistaModificaDipendente
from VisteAmministratore.VistaRicercaDipendente import VistaRicercaDipendente


class VistaGestioneDipendenti(QWidget):

    def __init__(self, parent=None):
        super(VistaGestioneDipendenti, self).__init__(parent)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_generic_button("Visualizza Lista Dipendenti", self.mostraListaDipendenti), 0, 0)
        grid_layout.addWidget(self.get_generic_button("Aggiungi Dipendente", self.aggiungiDipendente), 0, 1)
        grid_layout.addWidget(self.get_generic_button("Visualizza Dati Dipendente", self.mostraDatiDipendente), 1, 0)
        grid_layout.addWidget(self.get_generic_button("Modifica Dati Dipendente", self.modificaDipendente), 1, 1)
        grid_layout.addWidget(self.get_generic_button("Elimina Dipendente", self.eliminaDipendente), 2, 0)

        self.setLayout(grid_layout)
        self.resize(500,400)
        self.setWindowTitle("Gestione Dipendenti")

    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(on_click)
        return button

    def mostraListaDipendenti(self):
        self.vista_lista_dipendenti = VistaListaDipendenti()
        self.vista_lista_dipendenti.show()

    def aggiungiDipendente(self):
        self.vista_aggiungi = VistaAggiungiDipendente()
        self.vista_aggiungi.show()

    def mostraDatiDipendente(self):
        def apri_dettagli(dipendente):
            self.vista_dettagli = VistaDettagliDipendente(dipendente)
            self.vista_dettagli.show()

        self.vista_ricerca = VistaRicercaDipendente(on_dipendente_trovato=apri_dettagli)
        self.vista_ricerca.show()

    def modificaDipendente(self):
        def apri_modifica(dipendente):
            self.vista_modifica = VistaModificaDipendente(dipendente)
            self.vista_modifica.show()

        self.vista_ricerca = VistaRicercaDipendente(on_dipendente_trovato=apri_modifica)
        self.vista_ricerca.show()

    def eliminaDipendente(self):

        def apri_conferma(dipendente):
            self.vista_elimina = VistaConfermaEliminazioneDipendente(dipendente)
            self.vista_elimina.show()

        self.vista_ricerca = VistaRicercaDipendente(on_dipendente_trovato=apri_conferma)
        self.vista_ricerca.show()
